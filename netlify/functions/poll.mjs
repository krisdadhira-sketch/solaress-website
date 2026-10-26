// Poll votes for solaress.org. Counts are shared by all visitors and stored in Netlify Blobs.
// One vote per poll per visitor network address (hashed, never stored in clear); a visitor may change their vote.
// GET /api/poll?id=<poll>  -> {counts, total, mine}
// POST /api/poll?id=<poll> {"choice": "..."}  -> same, after recording the vote
import { getStore } from "@netlify/blobs";
import crypto from "node:crypto";

const POLLS = { "subsidy-50000": ["agree", "disagree", "undecided"] };
const json = (b, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { "content-type": "application/json", "cache-control": "no-store" } });

export default async (req, context) => {
  const id = new URL(req.url).searchParams.get("id");
  const opts = POLLS[id];
  if (!opts) return json({ error: "unknown poll" }, 400);
  const store = getStore({ name: "polls", consistency: "strong" });
  const ip = context.ip || req.headers.get("x-nf-client-connection-ip") || "";
  const h = crypto.createHash("sha256").update(`${id}|${ip}|solaress-poll-v1`).digest("hex").slice(0, 32);
  if (req.method === "POST") {
    let body = {};
    try { body = await req.json(); } catch (e) {}
    if (!opts.includes(body.choice)) return json({ error: "bad choice" }, 400);
    for (const o of opts) if (o !== body.choice) await store.delete(`${id}/${o}/${h}`);
    await store.set(`${id}/${body.choice}/${h}`, String(Date.now()));
  } else if (req.method !== "GET") return json({ error: "method" }, 405);
  const counts = {}; let mine = null, total = 0;
  for (const o of opts) {
    const { blobs } = await store.list({ prefix: `${id}/${o}/` });
    counts[o] = blobs.length; total += blobs.length;
    if (blobs.some((b) => b.key.endsWith("/" + h))) mine = o;
  }
  return json({ counts, total, mine });
};

export const config = { path: "/api/poll" };
