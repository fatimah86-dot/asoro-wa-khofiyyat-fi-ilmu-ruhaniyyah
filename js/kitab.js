(function () {
  const enter = document.getElementById("enter");
  const menu = document.getElementById("menu");
  const sidebar = document.getElementById("sidebar");
  const backdrop = document.getElementById("backdrop");

  function openBook() {
    document.body.classList.add("reading");
    const t = document.getElementById("catatan");
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
        links.forEach((l) =>
          l.classList.toggle("active", l.getAttribute("href") === "#" + e.target.id)
        );
      });
    },
    { rootMargin: "-20% 0px -70% 0px", threshold: 0 }
  );
  sections.forEach((s) => obs.observe(s));

  const leaves = ["naskah/Picture 001.jpg", "naskah/1.jpg"];
  for (let i = 2; i <= 149; i++) {
    const n = String(i).padStart(3, "0");
    leaves.push("naskah/Picture " + n + ".jpg");
  }

  const leaf = document.getElementById("leaf");
  const pager = document.getElementById("pager");
  const range = document.getElementById("range");
  if (range) {
    range.min = "0";
    range.max = String(leaves.length - 1);
  }
  let idx = 0;

  function show(i) {
    idx = Math.max(0, Math.min(leaves.length - 1, i));
    if (leaf) leaf.src = leaves[idx];
    if (pager) pager.textContent = idx + 1 + " / " + leaves.length;
    if (range) range.value = String(idx);
  }

  const prev = document.getElementById("prev");
  const next = document.getElementById("next");
  if (prev) prev.addEventListener("click", () => show(idx - 1));
  if (next) next.addEventListener("click", () => show(idx + 1));
  if (range) range.addEventListener("input", () => show(Number(range.value)));
})();
