// Actual Web Crypto checks in Node; synthetic private records, no browser/user data.
import assert from 'node:assert/strict';
import {PrivateVault, STORAGE_KEY} from '../web/vault.js';
function memory() { const store=new Map();return {getItem:key=>store.get(key)??null,setItem:(key,value)=>store.set(key,value)}; }
const record = {id:'ahv13',choice:'YES',notes:'SYNTHETIC-PRIVATE-NOTE-123',pinnedVersion:'source-version',savedAt:'2026-10-14T12:00:00Z',viewedUpdate:''};
const storage=memory(),vault=new PrivateVault(storage),password='Synthetic QA passphrase 2026';
await vault.create(password);await vault.save(record);
const raw=storage.getItem(STORAGE_KEY);
assert(!raw.includes(record.notes));assert(!raw.includes('ahv13'));assert(!raw.includes(password));assert.deepEqual(Object.keys(JSON.parse(raw)).sort(),['ciphertext','iterations','iv','kdf','salt','version']);
const firstIv=JSON.parse(raw).iv;await vault.save({...record,notes:'SYNTHETIC second note'});
assert.notEqual(JSON.parse(storage.getItem(STORAGE_KEY)).iv,firstIv);
vault.lock();assert.deepEqual(vault.entries,[]);assert.equal(vault.unlocked,false);
await assert.rejects(vault.unlock('Wrong password 1234'));assert.deepEqual(vault.entries,[]);
await vault.unlock(password);assert.equal(vault.entries[0].notes,'SYNTHETIC second note');
const tampered=JSON.parse(vault.backup());tampered.ciphertext=(tampered.ciphertext[0]==='A'?'B':'A')+tampered.ciphertext.slice(1);
await assert.rejects(vault.unlock(password,tampered));assert.equal(vault.unlocked,false);
await vault.unlock(password);await Promise.all([vault.save(record),vault.save({...record,id:'fireworks',notes:'SYNTHETIC other record'})]);
assert.equal(vault.entries.length,2);await vault.remove('fireworks');assert.equal(vault.entries.length,1);
const restored=new PrivateVault(memory());await restored.unlock(password,JSON.parse(vault.backup()));assert.deepEqual(restored.entries,vault.entries);
const unsafe=JSON.parse(vault.backup());unsafe.iterations=1;await assert.rejects(restored.unlock(password,unsafe));
const lockRace=new PrivateVault(memory());const pending=lockRace.create(password);lockRace.lock();await assert.rejects(pending);assert.equal(lockRace.exists,false);assert.equal(lockRace.unlocked,false);
await vault.unlock(password);const saving=vault.save({...record,notes:'SYNTHETIC cancelled write'});vault.lock();await assert.rejects(saving);
await vault.unlock(password);assert.notEqual(vault.entries[0].notes,'SYNTHETIC cancelled write');
console.log('PASS: encrypted-only persistence, fresh nonces, wrong-password/tamper rejection, lock/reload boundary, concurrent saves, backup recovery and cancelled lock races.');
