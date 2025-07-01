// api/index.js

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  const data = req.body;
  if (!data || typeof data !== 'object') {
    return res.status(400).send('Bad Request: JSON expected');
  }

  // Собираем текст из ключей и значений JSON
  const lines = Object.entries(data).map(
    ([key, val]) => `${key}: ${val}`
  );
  const text = lines.join('\n');

  const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
  const CHAT_ID  = process.env.TELEGRAM_CHAT_ID;
  const url      = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;

  try {
    const telegramRes = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: CHAT_ID, text })
    });

    if (!telegramRes.ok) {
      const errText = await telegramRes.text();
      console.error('Telegram API error:', errText);
      return res.status(telegramRes.status).send('Telegram API error');
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Internal error:', err);
    return res.status(500).send('Internal Server Error');
  }
}
