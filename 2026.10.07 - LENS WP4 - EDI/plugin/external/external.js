(function () {
  const External = {
    id: "external",

    init: async (deck) => {
      const revealEl = deck.getRevealElement();
      const placeholders = Array.from(
        revealEl.querySelectorAll("section[data-external]")
      );

      await Promise.all(
        placeholders.map(async (ph) => {
          const url = ph.getAttribute("data-external");
          if (!url) return;

          const res = await fetch(url);
          if (!res.ok) throw new Error(`External: failed to fetch ${url} (${res.status})`);

          const html = (await res.text()).trim();

          // Parse
          const container = document.createElement("div");
          container.innerHTML = html;

          // Prefer: the FIRST top-level <section> in the external file
          // (not nested sections)
          let rootSection = Array.from(container.children).find(
            (el) => el.tagName && el.tagName.toLowerCase() === "section"
          );

          // If the file wraps in a <div>, find the first <section> inside it
          if (!rootSection) {
            rootSection = container.querySelector(":scope > div > section");
          }

          // Fallback: wrap everything into one section
          if (!rootSection) {
            rootSection = document.createElement("section");
            rootSection.innerHTML = container.innerHTML;
          }

          ph.parentNode.insertBefore(rootSection, ph);
          ph.remove();
        })
      );
    },
  };

  window.External = External;
})();
