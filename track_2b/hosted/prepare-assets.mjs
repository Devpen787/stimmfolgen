// Deterministic public assets only. Secrets and local runtime state never enter this directory.
import {cp,copyFile,mkdir,readFile,writeFile,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const target=new URL('./.local/assets/',import.meta.url),demo=new URL('../demo/',import.meta.url);
const metadata=JSON.parse(await readFile(new URL('StimmFolgen_Live_Demo-metadata.json',demo),'utf8'));
const video=await readFile(new URL('StimmFolgen_Live_Demo.mp4',demo));
if(!Number.isFinite(metadata.duration_seconds)||metadata.duration_seconds<=0||metadata.duration_seconds>120||createHash('sha256').update(video).digest('hex')!==metadata.sha256)throw Error('Demo does not match reviewed media manifest');
await rm(target,{recursive:true,force:true});
await mkdir(target,{recursive:true});await cp(new URL('../web/',import.meta.url),target,{recursive:true});
await writeFile(new URL('demo.mp4',target),video);
await copyFile(new URL('./demo.html',import.meta.url),new URL('demo.html',target));
const srt=await readFile(new URL('StimmFolgen_Live_Demo.srt',demo),'utf8');
await writeFile(new URL('demo.vtt',target),'WEBVTT\n\n'+srt.replace(/(\d{2}:\d{2}:\d{2}),(\d{3})/g,'$1.$2'));
console.log('Prepared public website and hash-verified '+metadata.duration_seconds.toFixed(2)+'s demo. No credentials copied.');
