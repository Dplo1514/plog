document.addEventListener("DOMContentLoaded", function () {
    loadDocuments(1);
});

document.addEventListener("DOMContentLoaded", function () {
    const uploadModal = document.getElementById("uploadModal");
    const uploadForm = document.getElementById("upload-form");
    const fileInput = document.getElementById("file");
    const progressContainer = document.querySelector(".progress-container");

    // 모달 열기
    window.openUploadModal = function () {
        uploadModal.style.display = "flex";
    };

    // 모달 닫기
    window.closeUploadModal = function () {
        uploadModal.style.display = "none";
        clearProgressUI();
        loadDocuments(1)
    };

    // ESC 키로 모달 닫기
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeUploadModal();
        }
    });

    // 모달 외부 클릭 시 닫기
    uploadModal.addEventListener("click", function (event) {
        if (event.target === uploadModal) {
            closeUploadModal();
        }
    });

    // 폼 제출 이벤트 리스너 등록
    uploadForm.addEventListener("submit", handleFormSubmit);

    /**
     * 폼 제출 시 호출되는 함수
     */
    async function handleFormSubmit(event) {
        event.preventDefault();

        const files = fileInput.files;
        if (files.length === 0) {
            alert("Please select at least one file.");
            return;
        }

        clearProgressUI(); // 진행률 UI 초기화

        for (const file of files) {
            await uploadFile(file);
        }
    }

    /**
     * 파일을 업로드하는 함수
     * @param {File} file - 업로드할 파일 객체
     */
    async function uploadFile(file) {
        const {fileContainer, statusText, progressBar} = createProgressUI(file);
        progressContainer.appendChild(fileContainer);

        const chunkSize = 1024 * 1024; // 1MB
        const totalChunks = Math.ceil(file.size / chunkSize);

        try {
            for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
                const chunk = file.slice(
                    chunkIndex * chunkSize,
                    Math.min((chunkIndex + 1) * chunkSize, file.size)
                );
                const progress = await uploadChunk(file, chunk, chunkIndex,
                    chunkSize, totalChunks);

                progressBar.value = progress;
                statusText.innerText = `Uploading ${file.name}... ${progress}%`;

                if (progress === 100) {
                    statusText.innerText = `${file.name} Upload Complete!`;
                }
            }
        } catch (error) {
            statusText.innerText = `Error uploading ${file.name}: ${error.message}`;
        }
    }

    /**
     * 파일의 특정 청크(chunk)를 서버에 업로드
     * @param {File} file - 전체 파일 객체
     * @param {Blob} chunk - 업로드할 청크
     * @param {number} chunkIndex - 현재 청크의 인덱스
     * @param {number} chunkSize - 청크 크기
     * @param {number} totalChunks - 전체 청크 수
     * @returns {Promise<number>} - 업로드된 진행률 (퍼센트)
     */
    async function uploadChunk(file, chunk, chunkIndex, chunkSize,
        totalChunks) {
        const formData = new FormData();
        formData.append("file", chunk);
        formData.append("file_name", file.name);
        formData.append("file_size", file.size);
        formData.append("chunk_size", chunkSize);
        formData.append("chunk_index", chunkIndex);
        formData.append("total_chunk", totalChunks);

        const response = await fetch("/api/documents/upload", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Upload failed with status: ${response.status}`);
        }

        return Math.round(((chunkIndex + 1) / totalChunks) * 100); // 진행률 반환
    }

    /**
     * 개별 파일의 진행률 UI 생성
     * @param {File} file - 업로드할 파일 객체
     * @returns {{fileContainer: HTMLElement, statusText: HTMLElement, progressBar: HTMLElement}}
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

        return {fileContainer, statusText, progressBar};
    }

    /**
     * 진행률 UI를 초기화하는 함수
     */
    function clearProgressUI() {
        progressContainer.innerHTML = ""; // 진행률 UI 초기화
    }
});

function loadDocuments(page) {
    const searchQuery = document.getElementById("search").value || "";
    fetch(
        `/api/documents/list?page=${page}&q=${encodeURIComponent(searchQuery)}`)
    .then(response => response.json())
    .then(response => {
        const tableBody = document.getElementById("document-list");
        tableBody.innerHTML = "";

        response.data.data.forEach(doc => {
            const row = document.createElement("tr");
            row.innerHTML = `
                    <td>${doc.id}</td>
                    <td>${doc.name}</td>
                    <td>${doc.path}</td>
                    <td>${doc.status}</td>
                    <td>${doc.created_at}</td>
                    <td>${doc.modified_at}</td>
                `;
            tableBody.appendChild(row);
        });

        const pagination = document.getElementById("pagination");
        pagination.innerHTML = "";
        for (let i = 1;
            i <= Math.ceil(response.data.total / response.data.per_page); i++) {
            const pageBtn = document.createElement("button");
            pageBtn.className = `page-btn ${page === i ? "active" : ""}`;
            pageBtn.textContent = i;
            pageBtn.onclick = () => loadDocuments(i);
            pagination.appendChild(pageBtn);
        }
    })
    .catch(error => console.error("Error loading documents:", error));
}
