#!/usr/bin/env node
// Encrypts private/plan.json with a password you type, and writes plan.html.
// Usage: node tools/build_plan.mjs
// Crypto: PBKDF2-SHA256 (600k iterations) -> AES-256-GCM. The password is never stored.
import { readFileSync, writeFileSync } from "node:fs";
import { pbkdf2Sync, randomBytes, createCipheriv } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const ITER = 600000;

function ask(q) {
  return new Promise((resolve) => {
    process.stdout.write(q);
    const stdin = process.stdin;
    stdin.setRawMode?.(true); stdin.resume(); stdin.setEncoding("utf8");
    let buf = "";
    const onData = (c) => {
      for (const ch of c) {
        if (ch === "\r" || ch === "\n") { stdin.setRawMode?.(false); stdin.pause(); stdin.off("data", onData); process.stdout.write("\n"); return resolve(buf); }
        if (ch === "\u0003") process.exit(1);
        if (ch === "\u007f") buf = buf.slice(0, -1); else buf += ch;
      }
    };
    stdin.on("data", onData);
  });
}

const pw = process.env.PLAN_PASSWORD || await ask("Password for the training plan: ");
if (!process.env.PLAN_PASSWORD) {
  const again = await ask("Repeat password: ");
  if (pw !== again) { console.error("Passwords do not match."); process.exit(1); }
}
if (pw.length < 8) { console.error("Use at least 8 characters."); process.exit(1); }

const plain = readFileSync(join(root, "private/plan.json"));
const salt = randomBytes(16), iv = randomBytes(12);
const key = pbkdf2Sync(pw, salt, ITER, 32, "sha256");
const c = createCipheriv("aes-256-gcm", key, iv);
const ct = Buffer.concat([c.update(plain), c.final(), c.getAuthTag()]); // WebCrypto expects tag appended
const payload = JSON.stringify({ v: 1, iter: ITER, salt: salt.toString("base64"), iv: iv.toString("base64"), ct: ct.toString("base64") });

const tpl = readFileSync(join(root, "tools/plan_template.html"), "utf8");
if (!tpl.includes("/*__PAYLOAD__*/null")) throw new Error("template placeholder missing");
writeFileSync(join(root, "plan.html"), tpl.replace("/*__PAYLOAD__*/null", payload));
console.log("Wrote plan.html (encrypted). Commit plan.html; private/ stays local.");
