// api/index.js

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Only POST allowed');
  }

  const data = req.body;
  if (!data || typeof data !== 'object') {
    return res.status(400).send('Bad Request: JSON body expected');
  }

  // Превращаем пришедший JSON в строку
  const text = Object.entries(data)
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  const BOT_TOKEN = process.env.BOT_TOKEN;
  const CHAT_ID  = process.env.CHAT_ID;
  const url      = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;

  try {
    const telegramRes = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: CHAT_ID, text })
    });
    if (!telegramRes.ok) {
      const err = await telegramRes.text();
      console.error('Telegram API error:', err);
      return res.status(500).send('Telegram API error');
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Internal error:', e);
    return res.status(500).send('Internal Server Error');
  }
}
