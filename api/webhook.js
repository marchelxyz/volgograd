export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const data = req.body;

  const answers = (data?.form_response?.answers || [])
    .map(item => `${item.label || 'Вопрос'}: ${item.text || '...'}`)
    .join('\n');

  const BOT_TOKEN = process.env.BOT_TOKEN;
  const CHAT_ID = process.env.CHAT_ID;

  await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: CHAT_ID,
      text: answers || 'Новый ответ пришёл, но данных нет.'
    })
  });

  res.status(200).json({ status: 'ok' });
}