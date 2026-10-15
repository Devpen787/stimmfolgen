/* Private state stays in this browser. Only authenticated ciphertext is persisted. */
export const STORAGE_KEY = 'stimmfolgen.private.v1';
const AAD = new TextEncoder().encode('stimmfolgen-private-vault-v1');
const ITERATIONS = 600000;
const encode = bytes => btoa(String.fromCharCode(...bytes));
const decode = text => Uint8Array.from(atob(text), c => c.charCodeAt(0));
export function validateEnvelope(value) {
  if (!value || Object.keys(value).sort().join(',') !== 'ciphertext,iterations,iv,kdf,salt,version' ||
      value.version !== 1 || value.kdf !== 'PBKDF2-SHA256-AES256GCM' || value.iterations !== ITERATIONS ||
      typeof value.ciphertext !== 'string' || value.ciphertext.length > 1000000 ||
      decode(value.salt).length !== 16 || decode(value.iv).length !== 12 || decode(value.ciphertext).length < 16) {
    throw Error('Unsupported or damaged private backup.');
  }
  return value;
}
function validatePayload(value) {
  if (!value || value.version !== 1 || !Array.isArray(value.saved) || value.saved.length > 200) throw Error('Invalid private data.');
  for (const item of value.saved) {
    if (!/^[a-z0-9-]{1,60}$/.test(item.id) || typeof item.notes !== 'string' || item.notes.length > 16000 ||
        !['NOT_RECORDED','YES','NO','ABSTAIN'].includes(item.choice) || typeof item.pinnedVersion !== 'string' ||
        typeof item.savedAt !== 'string' || typeof item.viewedUpdate !== 'string') throw Error('Invalid saved vote.');
  }
  return value;
}
async function derive(password, salt) {
  const material = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:ITERATIONS,hash:'SHA-256'}, material,
    {name:'AES-GCM',length:256}, false, ['encrypt','decrypt']);
}
export class PrivateVault {
  constructor(storage = localStorage) { this.storage = storage; this.key = null; this.salt = null; this.data = null; this.generation = 0; this.pending = Promise.resolve(); }
  get exists() { return this.storage.getItem(STORAGE_KEY) !== null; }
  get unlocked() { return this.key !== null; }
  get entries() { return this.data?.saved || []; }
  lock() { this.generation++; this.key = null; this.salt = null; this.data = null; }
  async create(password) {
    if (this.exists) throw Error('Private data already exists. Unlock it instead.');
    if (password.length < 12) throw Error('Use a passphrase of at least 12 characters.');
    const generation = this.generation;
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await derive(password, salt);
    const data = {version:1,saved:[]};
    await this.persist(data,key,salt,generation);
    this.key = key; this.salt = salt; this.data = data;
  }
  async unlock(password, imported = null) {
    this.lock();
    const generation = this.generation;
    const envelope = validateEnvelope(imported || JSON.parse(this.storage.getItem(STORAGE_KEY)));
    const salt = decode(envelope.salt);
    const key = await derive(password,salt);
    let data;
    try { data = validatePayload(JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt(
      {name:'AES-GCM',iv:decode(envelope.iv),additionalData:AAD},key,decode(envelope.ciphertext))))); }
    catch { throw Error('Wrong passphrase or damaged private data. Nothing was unlocked.'); }
    if (generation !== this.generation) throw Error('Private operation cancelled by lock.');
    if (imported) this.storage.setItem(STORAGE_KEY,JSON.stringify(envelope));
    this.key = key; this.salt = salt; this.data = data;
  }
  async persist(data,key=this.key,salt=this.salt,generation=this.generation) {
    if (!key || !salt) throw Error('Unlock your private votes first.');
    validatePayload(data);
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const ciphertext = new Uint8Array(await crypto.subtle.encrypt({name:'AES-GCM',iv,additionalData:AAD},key,
      new TextEncoder().encode(JSON.stringify(data))));
    // Small records are capped above to avoid spreading very large arrays.
    const chunks = []; for (let i=0;i<ciphertext.length;i+=8192) chunks.push(String.fromCharCode(...ciphertext.subarray(i,i+8192)));
    const envelope = {version:1,kdf:'PBKDF2-SHA256-AES256GCM',iterations:ITERATIONS,salt:encode(salt),iv:encode(iv),ciphertext:btoa(chunks.join(''))};
    // Never persist a vault that the backup/unlock path would reject by size.
    if (JSON.stringify(envelope).length > 1000000) throw Error('Private vault is full. Download a backup before removing older records.');
    validateEnvelope(envelope);
    if (generation !== this.generation) throw Error('Private operation cancelled by lock.');
    this.storage.setItem(STORAGE_KEY,JSON.stringify(envelope));
  }
  change(action) {
    const generation = this.generation;
    const result = this.pending.catch(() => {}).then(async () => {
      if (!this.unlocked || generation !== this.generation) throw Error('Unlock your private votes first.');
      const next = {version:1,saved:action(this.entries)};
      await this.persist(next,this.key,this.salt,generation); this.data = next;
    });
    this.pending = result; return result;
  }
  async save(entry) { return this.change(items => items.filter(item => item.id !== entry.id).concat(entry)); }
  async remove(id) { return this.change(items => items.filter(item => item.id !== id)); }
  backup() { if (!this.exists) throw Error('No private backup is available.'); return this.storage.getItem(STORAGE_KEY); }
}
