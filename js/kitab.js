(function () {
  const enter = document.getElementById("enter");
  const menu = document.getElementById("menu");
  const sidebar = document.getElementById("sidebar");
  const backdrop = document.getElementById("backdrop");

  function openBook() {
    document.body.classList.add("reading");
    history.replaceState(null, "", "#muqaddimah");
    const t = document.getElementById("muqaddimah");
    if (t) t.scrollIntoView({ behavior: "instant", block: "start" });
  }

  if (enter) enter.addEventListener("click", openBook);

  if (location.hash && location.hash !== "#cover") {
    document.body.classList.add("reading");
  }

  function closeSide() {
    sidebar.classList.remove("open");
    backdrop.classList.remove("show");
  }
  if (menu) {
    menu.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      backdrop.classList.toggle("show");
    });
  }
  if (backdrop) backdrop.addEventListener("click", closeSide);
  sidebar.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeSide));

  const links = [...sidebar.querySelectorAll("a[href^='#']")];
  const sections = links
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  const obs = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        links.forEach((l) => l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id));
      });
    },
    { rootMargin: "-20% 0px -70% 0px", threshold: 0 }
  );
  sections.forEach((s) => obs.observe(s));
})();
