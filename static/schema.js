(function () {
    "use strict";

    function initializeSchemaDetail(container) {
        const detail = container.matches && container.matches("[data-schema-detail]")
            ? container
            : container.querySelector("[data-schema-detail]");

        if (!detail || detail.dataset.schemaInitialized === "true") return;
        detail.dataset.schemaInitialized = "true";

        const searchInput = detail.querySelector(".column-search-input");
        const searchCount = detail.querySelector(".column-search-count");
        const tableBody = detail.querySelector(".schema-column-table-body");
        const noResults = detail.querySelector(".no-column-results");

        if (searchInput && tableBody) {
            const rows = Array.from(tableBody.querySelectorAll(".column-row"));

            function filterColumns() {
                const query = searchInput.value.trim().toLowerCase();
                let visibleCount = 0;

                rows.forEach(function (row) {
                    const matches = row.textContent.toLowerCase().includes(query);
                    row.style.display = matches ? "" : "none";
                    if (matches) visibleCount += 1;
                });

                if (searchCount) searchCount.textContent = visibleCount;
                if (noResults) noResults.style.display = visibleCount === 0 ? "" : "none";
            }

            searchInput.addEventListener("input", filterColumns);
        }

        detail.addEventListener("click", async function (event) {
            const button = event.target.closest(".column-copy");
            if (!button || !detail.contains(button)) return;

            event.preventDefault();
            const columnName = button.dataset.column;
            if (!columnName) return;

            const icon = button.querySelector(".copy-icon");
            try {
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    await navigator.clipboard.writeText(columnName);
                } else {
                    throw new Error("Clipboard API unavailable");
                }
            } catch (error) {
                const temporaryInput = document.createElement("textarea");
                temporaryInput.value = columnName;
                temporaryInput.style.position = "fixed";
                temporaryInput.style.opacity = "0";
                document.body.appendChild(temporaryInput);
                temporaryInput.select();
                document.execCommand("copy");
                temporaryInput.remove();
            }

            button.classList.add("copied");
            if (icon) icon.textContent = "✓";
            window.setTimeout(function () {
                button.classList.remove("copied");
                if (icon) icon.textContent = "⧉";
            }, 1200);
        });
    }

    function setActiveTable(tableName) {
        document.querySelectorAll(".schema-table-item").forEach(function (item) {
            const isActive = item.dataset.tableName === tableName;
            item.classList.toggle("active", isActive);
            if (isActive) item.setAttribute("aria-current", "true");
            else item.removeAttribute("aria-current");
        });
    }

    async function loadInlineTable(link, pane) {
        const fullPageUrl = link.href;
        const requestUrl = new URL(fullPageUrl, window.location.origin);
        requestUrl.searchParams.set("partial", "1");

        pane.classList.add("is-loading");
        pane.setAttribute("aria-busy", "true");

        try {
            const response = await fetch(requestUrl.toString(), {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            });
            if (!response.ok) throw new Error("Unable to load table details");

            const html = await response.text();
            if (!html.includes("data-schema-detail")) {
                throw new Error("The table detail response was incomplete");
            }

            pane.innerHTML = html;
            pane.scrollTop = 0;
            initializeSchemaDetail(pane);
            setActiveTable(link.dataset.tableName || "");
        } catch (error) {
            // Keep the original full-page route as a graceful fallback.
            window.location.assign(fullPageUrl);
            return;
        } finally {
            pane.classList.remove("is-loading");
            pane.removeAttribute("aria-busy");
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll("[data-schema-detail]").forEach(initializeSchemaDetail);

        const detailPane = document.getElementById("schemaDetailPane");
        if (!detailPane) return;

        document.addEventListener("click", function (event) {
            const link = event.target.closest("a[data-schema-table], a[data-schema-inline-link]");
            if (!link || !detailPane.contains(link) && !link.hasAttribute("data-schema-table")) return;
            if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            if (link.target === "_blank") return;

            event.preventDefault();
            loadInlineTable(link, detailPane);
        });
    });
})();
