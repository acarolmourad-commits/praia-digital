<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit('Method not allowed');
}

$fields = ['empresa', 'nome', 'email', 'whatsapp', 'cidade', 'mensagem'];
$data = [];
foreach ($fields as $field) {
    $value = $_POST[$field] ?? '';
    $data[$field] = is_string($value) ? trim($value) : '';
}

$subject = $_POST['_subject'] ?? 'Novo pedido de parceria — Praia Digital';
$redirect = $_POST['_redirect'] ?? 'https://acarolmourad-commits.github.io/praia-digital/parcerias-imobiliarias-litoral-obrigado.html';

$to = getenv('PRAIA_DIGITAL_COMMERCIAL_EMAIL') ?: 'comercial@praia.digital';
$body = "Novo pedido\ Empresa: {$data['empresa']}\nNome: {$data['nome']}\nEmail: {$data['email']}\nWhatsApp: {$data['whatsapp']}\nCidade: {$data['cidade']}\nMensagem:\n{$data['mensagem']}";

$headers = [
    'Content-Type: text/plain; charset=utf-8',
    'From: Praia Digital <no-reply@praia.digital>',
    'Reply-To: ' . $data['email']
];

$mailSent = false;
if (!empty($data['email'])) {
    $mailSent = mail($to, $subject, $body, implode("\r\n", $headers));
}

header('Location: ' . $redirect);
exit;
