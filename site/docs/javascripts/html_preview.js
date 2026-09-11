/* The text and its styles are present in the initial HTML. This only adds controls. */
(() => {
  class PDFPreview extends HTMLElement {
    connectedCallback() {
      if (this.observer) return;
      // Also handles themes that replace content with innerHTML on navigation:
      // that API leaves declarative templates inert rather than attaching them.
      if (!this.shadowRoot) {
        const template = this.querySelector('template[shadowrootmode]');
        if (!template) return;
        this.attachShadow({mode: 'open'}).append(template.content.cloneNode(true));
        template.remove();
      }
      const root = this.shadowRoot;
      const pages = root.querySelector('.pages');
      this.zoom = 1;
      const frames = [...root.querySelectorAll('.page-frame')];
      const dimensions = frames.map(frame => {
        const page = frame.querySelector('.pf');
        return {frame, page, width: page.offsetWidth, height: page.offsetHeight};
      });
      const select = root.querySelector('select');
      const resize = () => {
        const available = pages.clientWidth;
        if (!available) return;
        for (const {frame, page, width, height} of dimensions) {
          const scale = available / width * this.zoom;
          page.style.transform = `scale(${scale})`;
          page.style.position = 'absolute';
          frame.style.width = `${width * scale}px`;
          frame.style.height = `${height * scale + 24}px`;
          frame.querySelector('.page-caption').style.paddingTop = `${height * scale}px`;
        }
        root.querySelector('[data-action="out"]').disabled = this.zoom <= 1;
        root.querySelector('[data-action="in"]').disabled = this.zoom >= 3;
      };
      select.addEventListener('change', () => frames[Number(select.value) - 1].scrollIntoView({block:'start'}));
      root.querySelector('.toolbar').addEventListener('click', event => {
        const action = event.target.dataset.action;
        if (!action) return;
        this.zoom = action === 'fit' ? 1 : Math.min(3, Math.max(1, this.zoom + (action === 'in' ? .25 : -.25)));
        resize();
      });
      // PDF link overlays use destination coordinates in data-dest-detail.
      root.addEventListener('click', event => {
        const link = event.target.closest('a');
        if (!link || !link.getAttribute('href')?.startsWith('#')) return;
        const target = root.getElementById(link.getAttribute('href').slice(1));
        if (target) { event.preventDefault(); target.scrollIntoView({block:'start'}); }
      });
      this.observer = new ResizeObserver(resize);
      this.observer.observe(pages);
      this.observePages = () => {
        this.pageObserver?.disconnect();
        this.pageObserver = new IntersectionObserver(entries => {
          const visible = entries.filter(entry => entry.isIntersecting);
          if (visible.length) select.value = visible[0].target.dataset.page;
        // Use pixels: percentage root margins are based on width, not height.
        }, {rootMargin: `${-innerHeight * .30}px 0px ${-innerHeight * .69}px 0px`});
        frames.forEach(frame => this.pageObserver.observe(frame));
      };
      this.observePages();
      window.addEventListener('resize', this.observePages);
      root.querySelector('.toolbar').hidden = false;
      resize();
    }
    disconnectedCallback() {
      this.observer?.disconnect();
      this.pageObserver?.disconnect();
      window.removeEventListener('resize', this.observePages);
      this.observer = null;
    }
  }
  if (!customElements.get('hku-pdf-preview')) customElements.define('hku-pdf-preview', PDFPreview);
})();
