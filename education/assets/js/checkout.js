/**
 * Course catalog for Praia Digital Academy checkout.
 * In production, this can be fetched from /education/cursos/assets-gerados.json
 * or an external API endpoint.
 */
const COURSE_CATALOG = {
  "airbnb-do-zero": {
    id: "airbnb-do-zero",
    slug: "airbnb-do-zero",
    title: "Airbnb do Zero no Litoral — Praia Digital Academy",
    price: 29700,
    priceOriginal: 39700,
    cover: "https://praia.digital/img/courses/airbnb-do-zero.jpg",
    description: "Aprenda a montar, operar e escalar um Airbnb de sucesso no litoral paulista.",
    category: "temporada"
  },
  "booking-do-zero": {
    id: "booking-do-zero",
    slug: "booking-do-zero",
    title: "Booking do Zero no Litoral — Praia Digital Academy",
    price: 29700,
    priceOriginal: 39700,
    cover: "https://praia.digital/img/courses/booking-do-zero.jpg",
    description: "Domine a plataforma Booking e aumente a ocupação do seu imóvel na praia.",
    category: "temporada"
  },
  "analise-de-mercado-imobiliario-litoral": {
    id: "analise-de-mercado-imobiliario-litoral",
    slug: "analise-de-mercado-imobiliario-litoral",
    title: "Análise de Mercado Imobiliário no Litoral — Praia Digital Academy",
    price: 34700,
    priceOriginal: 44700,
    cover: "https://praia.digital/img/courses/analise-de-mercado.jpg",
    description: "Aprenda a ler o mercado litorâneo, identificar oportunidades e tomar decisões seguras.",
    category: "investimento"
  },
  "analise-de-rentabilidade": {
    id: "analise-de-rentabilidade",
    slug: "analise-de-rentabilidade",
    title: "Análise de Rentabilidade no Litoral — Praia Digital Academy",
    price: 34700,
    priceOriginal: 44700,
    cover: "https://praia.digital/img/courses/analise-rentabilidade.jpg",
    description: "Calcule rentabilidade real de imóveis na praia: yield, custos e retorno.",
    category: "investimento"
  },
  "avaliacao-de-imoveis": {
    id: "avaliacao-de-imoveis",
    slug: "avaliacao-de-imoveis",
    title: "Avaliação de Imóveis no Litoral — Praia Digital Academy",
    price: 29700,
    priceOriginal: 39700,
    cover: "https://praia.digital/img/courses/avaliacao-imoveis.jpg",
    description: "Aprenda a precificar imóveis de praia com método e dados de mercado.",
    category: "avaliacao"
  },
  "default": {
    id: "default",
    slug: "curso",
    title: "Curso — Praia Digital Academy",
    price: 29700,
    priceOriginal: 39700,
    cover: "https://praia.digital/img/default-home.jpg",
    description: "Conteúdo prático para o mercado imobiliário do litoral.",
    category: "geral"
  }
};

/**
 * Payment gateway abstraction.
 * Replace simulated methods with real API calls to your gateway:
 * - MercadoPago
 * - Pagar.me
 * - Stripe
 * - Adyen
 * - etc.
 */
const PaymentGateway = {
  config: {
    currency: 'BRL',
    maxInstallments: 12,
    interestRate: 2.99, // monthly interest rate in %
    pixDiscount: 5, // discount percentage for PIX
    webhookEndpoint: '/api/webhooks/payment',
    apiEndpoint: '/api/payments'
  },

  /**
   * Create PIX payment - returns QR code and copy-paste code
   */
  async createPix(amount, buyer) {
    // TODO: Replace with real gateway API call
    // Example: POST /api/payments/pix { amount, buyer, course_id }
    
    const qrCodeData = `00020126580014br.gov.bcb.pix0136${buyer.email}520400005303986540${amount}005802BR5925Praia Digital Academy6009Sao Paulo62070503***6304`;
    
    // Simulated response - in production this comes from your gateway
    return {
      method: 'pix',
      status: 'pending',
      qrCode: `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(qrCodeData)}`,
      qrCodeRaw: qrCodeData,
      expiresAt: new Date(Date.now() + 30 * 60 * 1000).toISOString(), // 30 min
      paymentId: `pix_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`
    };
  },

  /**
   * Create credit card payment with tokenization
   */
  async createCard(amount, cardData, buyer, installments) {
    // TODO: Replace with real gateway tokenization
    // 1. Tokenize card on frontend with gateway SDK
    // 2. Send token + installments to backend
    // 3. Backend creates payment intent
    
    const calculatedAmount = this.calculateInstallmentAmount(amount, installments);
    
    return {
      method: 'credit_card',
      status: 'pending',
      installments: installments,
      installmentAmount: calculatedAmount.installmentAmount,
      totalAmount: calculatedAmount.totalAmount,
      paymentId: `card_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`
    };
  },

  /**
   * Calculate installment amount with interest
   */
  calculateInstallmentAmount(baseAmount, installments) {
    const monthlyRate = this.config.interestRate / 100;
    
    if (installments === 1) {
      return {
        installmentAmount: baseAmount,
        totalAmount: baseAmount,
        hasInterest: false
      };
    }
    
    // Compound interest formula
    const totalAmount = baseAmount * Math.pow(1 + monthlyRate, installments);
    const installmentAmount = totalAmount / installments;
    
    return {
      installmentAmount: Math.round(installmentAmount * 100) / 100,
      totalAmount: Math.round(totalAmount * 100) / 100,
      hasInterest: true
    };
  },

  /**
   * Calculate PIX discounted amount
   */
  calculatePixAmount(baseAmount) {
    const discount = baseAmount * (this.config.pixDiscount / 100);
    return Math.round((baseAmount - discount) * 100) / 100;
  },

  /**
   * Poll payment status - simulates webhook listener
   */
  async pollPaymentStatus(paymentId) {
    // TODO: Replace with real status check
    // GET /api/payments/{paymentId}/status
    
    // Simulated polling - in production use webhooks instead
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          paymentId,
          status: 'approved', // or 'pending', 'rejected', 'cancelled'
          approvedAt: new Date().toISOString(),
          transactionId: `tx_${Date.now()}`
        });
      }, 2000);
    });
  },

  /**
   * Send order metadata to CRM/student management system
   */
  async sendToCRM(orderData) {
    // TODO: Integrate with your CRM/student platform
    // POST /api/crm/enroll { orderData }
    
    console.log('CRM integration - Order data:', orderData);
    
    return {
      success: true,
      studentId: `student_${Date.now()}`,
      accessUrl: `/education/aluno/index.html`
    };
  }
};

/**
 * Form validator with real-time validation
 */
const FormValidator = {
  masks: {
    phone: (value) => {
      return value
        .replace(/\D/g, '')
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{5})(\d)/, '$1-$2')
        .slice(0, 15);
    },
    document: (value) => {
      const numbers = value.replace(/\D/g, '');
      if (numbers.length <= 11) {
        return numbers
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d)/, '$1.$2')
          .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
          .slice(0, 14);
      }
      return numbers
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1/$2')
        .replace(/(\d{4})(\d{1,2})$/, '$1-$2')
        .slice(0, 18);
    }
  },

  validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  validatePhone(phone) {
    const numbers = phone.replace(/\D/g, '');
    return numbers.length >= 10 && numbers.length <= 11;
  },

  validateDocument(doc) {
    const numbers = doc.replace(/\D/g, '');
    return numbers.length === 11 || numbers.length === 14;
  },

  validateName(name) {
    return name.trim().length >= 3;
  },

  validateForm(data) {
    const errors = [];
    
    if (!this.validateName(data.name)) {
      errors.push('Nome completo é obrigatório');
    }
    
    if (!this.validateEmail(data.email)) {
      errors.push('E-mail inválido');
    }
    
    if (data.email !== data.emailConfirm) {
      errors.push('E-mails não coincidem');
    }
    
    if (!this.validatePhone(data.phone)) {
      errors.push('Telefone/WhatsApp inválido');
    }
    
    if (!this.validateDocument(data.document)) {
      errors.push('CPF/CNPJ inválido');
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
};

/**
 * Checkout controller - main logic
 */
const CheckoutController = {
  currentCourse: null,
  selectedPayment: null,
  orderId: null,

  init() {
    this.loadCourseFromURL();
    this.setupEventListeners();
    this.setupFormValidation();
  },

  loadCourseFromURL() {
    const params = new URLSearchParams(location.search);
    const slug = params.get('slug');
    const title = params.get('title');
    const price = params.get('price');
    
    // Try to load from catalog by slug
    if (slug && COURSE_CATALOG[slug]) {
      this.currentCourse = { ...COURSE_CATALOG[slug] };
    } else if (slug && COURSE_CATALOG['default']) {
      // Use default but override with URL params if provided
      this.currentCourse = { 
        ...COURSE_CATALOG['default'],
        slug: slug,
        title: title ? decodeURIComponent(title) : COURSE_CATALOG['default'].title
      };
    } else {
      // No valid slug - redirect to catalog
      setTimeout(() => {
        location.href = '/education/';
      }, 3000);
      this.showError('Curso não encontrado. Redirecionando para o catálogo...');
      return;
    }
    
    // Override price if provided in URL
    if (price && !isNaN(parseInt(price))) {
      this.currentCourse.price = parseInt(price) * 100; // convert to cents
    }
    
    this.renderCourseInfo();
    this.updatePricing();
  },

  renderCourseInfo() {
    if (!this.currentCourse) return;
    
    const courseName = document.getElementById('course-name');
    const courseDescription = document.getElementById('course-description');
    const courseCover = document.getElementById('course-cover');
    
    if (courseName) courseName.textContent = this.currentCourse.title;
    if (courseDescription) courseDescription.textContent = this.currentCourse.description;
    if (courseCover) courseCover.src = this.currentCourse.cover;
  },

  updatePricing() {
    if (!this.currentCourse) return;
    
    const basePrice = this.currentCourse.price / 100; // convert from cents
    const pixPrice = PaymentGateway.calculatePixAmount(basePrice);
    
    document.getElementById('course-price').textContent = this.formatCurrency(basePrice);
    document.getElementById('course-price-original').textContent = this.formatCurrency(this.currentCourse.priceOriginal / 100);
    document.getElementById('course-price-pix').textContent = this.formatCurrency(pixPrice);
  },

  formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },

  setupEventListeners() {
    // Payment method selection
    const paymentMethods = document.querySelectorAll('input[name="payment-method"]');
    paymentMethods.forEach(method => {
      method.addEventListener('change', (e) => {
        this.selectedPayment = e.target.value;
        this.showPaymentForm();
      });
    });
    
    // Installment selector
    const installmentSelect = document.getElementById('installments');
    if (installmentSelect) {
      installmentSelect.addEventListener('change', (e) => {
        this.updateInstallmentPreview(parseInt(e.target.value));
      });
    }
    
    // Form submission
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
      checkoutForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.processPayment();
      });
    }
  },

  setupFormValidation() {
    // Phone mask
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
      phoneInput.addEventListener('input', (e) => {
        e.target.value = FormValidator.masks.phone(e.target.value);
      });
    }
    
    // Document mask
    const docInput = document.getElementById('document');
    if (docInput) {
      docInput.addEventListener('input', (e) => {
        e.target.value = FormValidator.masks.document(e.target.value);
      });
    }
    
    // Email confirmation
    const emailInput = document.getElementById('email');
    const emailConfirmInput = document.getElementById('email-confirm');
    if (emailInput && emailConfirmInput) {
      emailConfirmInput.addEventListener('input', () => {
        this.validateEmailMatch();
      });
    }
  },

  validateEmailMatch() {
    const email = document.getElementById('email').value;
    const confirm = document.getElementById('email-confirm').value;
    const errorEl = document.getElementById('email-confirm-error');
    
    if (confirm && email !== confirm) {
      errorEl.style.display = 'block';
      return false;
    }
    
    errorEl.style.display = 'none';
    return true;
  },

  showPaymentForm() {
    const pixForm = document.getElementById('pix-form');
    const cardForm = document.getElementById('card-form');
    
    if (this.selectedPayment === 'pix') {
      pixForm.style.display = 'block';
      cardForm.style.display = 'none';
      this.generatePixQR();
    } else if (this.selectedPayment === 'card') {
      pixForm.style.display = 'none';
      cardForm.style.display = 'block';
      this.populateInstallments();
    }
  },

  async generatePixQR() {
    if (!this.currentCourse) return;
    
    const basePrice = this.currentCourse.price / 100;
    const pixPrice = PaymentGateway.calculatePixAmount(basePrice);
    
    try {
      const pixData = await PaymentGateway.createPix(pixPrice * 100, {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        document: document.getElementById('document').value
      });
      
      document.getElementById('qr-code').src = pixData.qrCode;
      document.getElementById('qr-code-raw').textContent = pixData.qrCodeRaw;
      document.getElementById('pix-expires').textContent = new Date(pixData.expiresAt).toLocaleTimeString('pt-BR');
      this.orderId = pixData.paymentId;
      
      // Start polling for payment confirmation
      this.startPaymentPolling(pixData.paymentId);
    } catch (error) {
      this.showError('Erro ao gerar QR Code PIX. Tente novamente.');
    }
  },

  populateInstallments() {
    if (!this.currentCourse) return;
    
    const basePrice = this.currentCourse.price / 100;
    const select = document.getElementById('installments');
    select.innerHTML = '';
    
    for (let i = 1; i <= PaymentGateway.config.maxInstallments; i++) {
      const calc = PaymentGateway.calculateInstallmentAmount(basePrice * 100, i);
      const option = document.createElement('option');
      option.value = i;
      option.textContent = `${i}x de ${this.formatCurrency(calc.installmentAmount)}${i > 1 ? ' (total: ' + this.formatCurrency(calc.totalAmount) + ')' : ' (sem juros)'}`;
      select.appendChild(option);
    }
    
    this.updateInstallmentPreview(1);
  },

  updateInstallmentPreview(installments) {
    if (!this.currentCourse) return;
    
    const basePrice = this.currentCourse.price / 100;
    const calc = PaymentGateway.calculateInstallmentAmount(basePrice * 100, installments);
    
    document.getElementById('installment-preview').textContent = 
      `${installments}x de ${this.formatCurrency(calc.installmentAmount)}`;
    document.getElementById('installment-total').textContent = 
      `Total: ${this.formatCurrency(calc.totalAmount)}`;
  },

  async processPayment() {
    // Validate form
    const formData = {
      name: document.getElementById('name').value,
      email: document.getElementById('email').value,
      emailConfirm: document.getElementById('email-confirm')?.value || '',
      phone: document.getElementById('phone').value,
      document: document.getElementById('document').value
    };
    
    const validation = FormValidator.validateForm(formData);
    if (!validation.valid) {
      this.showError(validation.errors.join('<br>'));
      return;
    }
    
    // Disable button during processing
    const submitBtn = document.getElementById('submit-payment');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Processando...';
    
    try {
      let paymentResult;
      
      if (this.selectedPayment === 'pix') {
        paymentResult = await PaymentGateway.createPix(
          PaymentGateway.calculatePixAmount(this.currentCourse.price / 100) * 100,
          formData
        );
      } else if (this.selectedPayment === 'card') {
        const installments = parseInt(document.getElementById('installments').value);
        paymentResult = await PaymentGateway.createCard(
          this.currentCourse.price,
          { token: 'card_token_placeholder' }, // TODO: Get real token from gateway SDK
          formData,
          installments
        );
      }
      
      this.orderId = paymentResult.paymentId;
      
      // Send to CRM
      const crmResult = await PaymentGateway.sendToCRM({
        slug: this.currentCourse.slug,
        title: this.currentCourse.title,
        customer: formData,
        payment: paymentResult,
        orderId: this.orderId
      });
      
      // Wait for payment confirmation
      await this.waitForPaymentConfirmation();
      
      // Redirect to thank you page
      this.redirectToThankYou(crmResult);
      
    } catch (error) {
      this.showError('Erro ao processar pagamento. Tente novamente.');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Confirmar pagamento';
    }
  },

  async waitForPaymentConfirmation() {
    const maxAttempts = 60; // 5 minutes max
    const interval = 5000; // 5 seconds
    
    for (let i = 0; i < maxAttempts; i++) {
      const status = await PaymentGateway.pollPaymentStatus(this.orderId);
      
      if (status.status === 'approved') {
        return status;
      } else if (status.status === 'rejected' || status.status === 'cancelled') {
        throw new Error('Pagamento não aprovado');
      }
      
      // Update UI with waiting message
      const statusEl = document.getElementById('payment-status');
      if (statusEl) {
        statusEl.textContent = `Aguardando confirmação... (${(i + 1) * 5}s)`;
      }
      
      await new Promise(resolve => setTimeout(resolve, interval));
    }
    
    throw new Error('Timeout na confirmação do pagamento');
  },

  redirectToThankYou(crmResult) {
    const params = new URLSearchParams({
      slug: this.currentCourse.slug,
      title: this.currentCourse.title,
      status: 'success',
      orderId: this.orderId,
      studentId: crmResult.studentId
    });
    
    location.href = `/education/thank-you.html?${params.toString()}`;
  },

  showError(message) {
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.innerHTML = `<p><strong>Erro</strong></p><p>${message}</p>`;
    result.style.background = 'rgba(255, 100, 100, 0.1)';
    result.style.border = '1px solid rgba(255, 100, 100, 0.3)';
  },

  showSuccess(message) {
    const result = document.getElementById('result');
    result.style.display = 'block';
    result.innerHTML = `<p><strong>Sucesso!</strong></p><p>${message}</p>`;
    result.style.background = 'rgba(100, 255, 100, 0.1)';
    result.style.border = '1px solid rgba(100, 255, 100, 0.3)';
  }
};

// Initialize checkout when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => CheckoutController.init());
} else {
  CheckoutController.init();
}
