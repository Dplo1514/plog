document.addEventListener("DOMContentLoaded", function () {
    setupEventListeners();
    loadDocuments(1);
});

/**
 * 초기 이벤트 리스너 설정
 */
function setupEventListeners() {
    const uploadModal = document.getElementById("uploadModal");
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file");
    const progressContainer = document.querySelector(".progress-container");

    // 모달 열기 & 닫기
    window.openUploadModal = () => (uploadModal.style.display = "flex");
    window.closeUploadModal = () => {
        uploadModal.style.display = "none";
        clearProgressUI();
        loadDocuments(1);
    };

    // ESC 키로 모달 닫기
    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeUploadModal();
    });

    // 모달 외부 클릭 시 닫기
    uploadModal.addEventListener("click", (event) => {
        if (event.target === uploadModal) closeUploadModal();
    });

    // 파일 업로드 이벤트 리스너
    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            alert("📂 Please select at least one file.");
            return;
        }

        clearProgressUI();
        for (const file of files) await uploadFile(file);
    });

    // 🔹 상태 필터 버튼 클릭 이벤트 추가
    document.querySelectorAll(".status-filter-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
            document.querySelectorAll(".status-filter-btn").forEach((b) => b.classList.remove("active"));
            this.classList.add("active");

            const selectedStatus = this.dataset.status || "";
            loadDocuments(1, selectedStatus);
        });
    });

    // 🔹 검색 버튼 클릭 시 문서 로드
    document.getElementById("search-btn").addEventListener("click", () => {
        const selectedStatus = document.querySelector(".status-filter-btn.active").dataset.status || "";
        loadDocuments(1, selectedStatus);
    });
}

/**
 * 문서 목록을 불러오는 함수
 */
function loadDocuments(page = 1, status = "") {
    const searchQuery = document.getElementById("search").value.trim();

    fetch(`/api/documents/list?status=${status}&page=${page}&q=${encodeURIComponent(searchQuery)}`)
    .then((response) => response.json())
    .then((response) => {
        const tableBody = document.getElementById("document-list");
        tableBody.innerHTML = "";

        response.data.data.forEach((doc) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                    <td>${doc.id}</td>
                    <td>${doc.name}</td>
                    <td>${doc.path}</td>
                    <td class="status-${doc.status.toLowerCase()}">${doc.status}</td>
                    <td>${doc.created_at}</td>
                    <td>${doc.modified_at}</td>
                `;
            tableBody.appendChild(row);
        });

        renderPagination(response.data.total, response.data.per_page, page, status);
    })
    .catch((error) => console.error("Error loading documents:", error));
}

/**
 * 파일 업로드
 */
async function uploadFile(file) {
    const { fileContainer, statusText, progressBar } = createProgressUI(file);
    document.querySelector(".progress-container").appendChild(fileContainer);

    const chunkSize = 1024 * 1024; // 1MB
    const totalChunks = Math.ceil(file.size / chunkSize);

    try {
        for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
            const chunk = file.slice(chunkIndex * chunkSize, Math.min((chunkIndex + 1) * chunkSize, file.size));
            const progress = await uploadChunk(file, chunk, chunkIndex, chunkSize, totalChunks);

            progressBar.value = progress;
            statusText.innerText = `Uploading ${file.name}... ${progress}%`;

            if (progress === 100) statusText.innerText = `${file.name} ✅ Upload Complete!`;
        }
    } catch (error) {
        statusText.innerText = `❌ Error uploading ${file.name}: ${error.message}`;
    }
}

/**
 * 파일 청크 업로드
 */
async function uploadChunk(file, chunk, chunkIndex, chunkSize, totalChunks) {
    const formData = new FormData();
    formData.append("file", chunk);
    formData.append("file_name", file.name);
    formData.append("file_size", file.size);
    formData.append("chunk_size", chunkSize);
    formData.append("chunk_index", chunkIndex);
    formData.append("total_chunk", totalChunks);

    const response = await fetch("/api/documents/upload", { method: "POST", body: formData });

    if (!response.ok) throw new Error(`Upload failed with status: ${response.status}`);

    return Math.round(((chunkIndex + 1) / totalChunks) * 100);
}

/**
 * 진행률 UI 생성
 */
function createProgressUI(file) {
    const fileContainer = document.createElement("div");
    fileContainer.classList.add("file-progress");

    const statusText = document.createElement("p");
    statusText.innerText = `Uploading ${file.name}...`;
    fileContainer.appendChild(statusText);

    const progressBar = document.createElement("progress");
    progressBar.value = 0;
    progressBar.max = 100;
    fileContainer.appendChild(progressBar);

    return { fileContainer, statusText, progressBar };
}

/**
 * 진행률 UI 초기화
 */
function clearProgressUI() {
    document.querySelector(".progress-container").innerHTML = "";
}

/**
 * 페이지네이션 렌더링
 */
function renderPagination(total, perPage, currentPage, status) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const totalPages = Math.ceil(total / perPage);
    for (let i = 1; i <= totalPages; i++) {
        const pageBtn = document.createElement("button");
        pageBtn.className = `page-btn ${currentPage === i ? "active" : ""}`;
        pageBtn.textContent = i;
        pageBtn.onclick = () => loadDocuments(i, status);
        pagination.appendChild(pageBtn);
    }
}