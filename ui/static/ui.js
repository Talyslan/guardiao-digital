document.addEventListener('DOMContentLoaded', function () {
  function attachForm(formSelector, validator) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    const submit = form.querySelector('button[type="submit"]');
    const spinner = document.createElement('span');
    spinner.className = 'spinner';
    spinner.style.display = 'none';
    spinner.style.marginLeft = '8px';
    submit.appendChild(spinner);

    const errorBox = document.createElement('div');
    errorBox.className = 'flash danger';
    errorBox.style.display = 'none';
    form.insertBefore(errorBox, form.firstChild);

    form.addEventListener('submit', function (ev) {
      // client-side validation: validator should return {ok:bool, msg?:string}
      if (typeof validator === 'function') {
        const res = validator(form);
        if (!res.ok) {
          ev.preventDefault();
          errorBox.innerText = res.msg || 'Informe os campos corretamente.';
          errorBox.style.display = 'block';
          return false;
        }
      }

      // hide existing errors and show spinner
      errorBox.style.display = 'none';
      submit.disabled = true;
      spinner.style.display = 'inline-block';
      return true;
    });
  }

  // validator: at least one of text or url must be present
  attachForm('#analyze-form', function (form) {
    const text = form.querySelector('textarea[name="text"]').value.trim();
    const url = form.querySelector('input[name="url"]').value.trim();
    if (!text && !url) {
      return { ok: false, msg: 'Por favor informe um texto ou uma URL para analisar.' };
    }
    return { ok: true };
  });

  attachForm('#phishing-form', function (form) {
    const textEl = form.querySelector('textarea[name="text"]');
    const urlEl = form.querySelector('input[name="url"]');
    const emailEl = form.querySelector('input[name="email"]');
    const text = textEl ? textEl.value.trim() : '';
    const url = urlEl ? urlEl.value.trim() : '';
    const email = emailEl ? emailEl.value.trim() : '';
    if (!text && !url && !email) {
      return { ok: false, msg: 'Informe pelo menos um campo (texto, URL ou email).' };
    }
    return { ok: true };
  });
});
