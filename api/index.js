// api/index.js
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Only POST allowed');
  }

  // Yandex может слать либо { params: {Имя:...,Телефон:...} } (JSON-RPC)
  // либо { form_response: { answers: [...] } } (Webhook)
  const body = req.body;
  let data = {};

  if (body.params && typeof body.params === 'object') {
    // JSON-RPC mode
    data = body.params;
  } else if (body.form_response && Array.isArray(body.form_response.answers)) {
    // Webhook mode
    body.form_response.answers.forEach(ans => {
      data[ans.label] = ans.text || ans.email || ans.string || '';
    });
  } else {
    return res.status(400).send('Bad Request: unknown payload');
  }

  // Собираем текст сообщения
  const lines = Object.entries(data).map(([k, v]) => `${k}: ${v}`);
  const text  = ['Новая бронь:', ...lines].join('\n');

  const BOT_TOKEN = process.env.BOT_TOKEN;
  const CHAT_ID  = process.env.CHAT_ID;
  const url      = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;

  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: CHAT_ID, text })
    });
    if (!r.ok) {
      const err = await r.text();
      console.error('Telegram API error:', err);
      return res.status(502).send('Telegram error');
    }
    return res.status(200).json({ ok: true });
  } catch (e) {
    console.error('Internal error:', e);
    return res.status(500).send('Internal Server Error');
  }
}
