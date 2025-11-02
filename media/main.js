// @ts-check

(function () {
    // @ts-ignore
    const vscode = acquireVsCodeApi();

    let allVectors = [];
    let filteredVectors = [];
    let currentPage = 1;
    const itemsPerPage = 50;
    let sortColumn = 'id';
    let sortDirection = 'asc';

    // DOM Elements
    const searchBox = document.getElementById('search-box');
    const tableBody = document.getElementById('table-body');
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const vectorTable = document.getElementById('vector-table');
    const dbType = document.getElementById('db-type');
    const dbCount = document.getElementById('db-count');
    const dbDimension = document.getElementById('db-dimension');
    const refreshBtn = document.getElementById('refresh-btn');
    const exportBtn = document.getElementById('export-btn');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfo = document.getElementById('page-info');

    // Modal elements
    const textModal = document.getElementById('text-modal');
    const closeModal = document.getElementById('close-modal');
    const modalId = document.getElementById('modal-id');
    const modalSource = document.getElementById('modal-source');
    const modalLength = document.getElementById('modal-length');
    const modalText = document.getElementById('modal-text');
    const copyTextBtn = document.getElementById('copy-text-btn');

    const vectorModal = document.getElementById('vector-modal');
    const closeVectorModal = document.getElementById('close-vector-modal');
    const vectorModalId = document.getElementById('vector-modal-id');
    const vectorDimensions = document.getElementById('vector-dimensions');
    const vectorDisplay = document.getElementById('vector-display');
    const copyVectorBtn = document.getElementById('copy-vector-btn');

    // Event Listeners
    searchBox.addEventListener('input', handleSearch);
    refreshBtn.addEventListener('click', handleRefresh);
    exportBtn.addEventListener('click', handleExport);
    prevPageBtn.addEventListener('click', () => changePage(-1));
    nextPageBtn.addEventListener('click', () => changePage(1));

    // Table sorting
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            handleSort(column);
        });
    });

    // Modal close handlers
    closeModal.addEventListener('click', () => {
        textModal.style.display = 'none';
    });

    closeVectorModal.addEventListener('click', () => {
        vectorModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === textModal) {
            textModal.style.display = 'none';
        }
        if (event.target === vectorModal) {
            vectorModal.style.display = 'none';
        }
    });

    // Handle messages from extension
    window.addEventListener('message', event => {
        const message = event.data;
        
        switch (message.type) {
            case 'vectorData':
                handleVectorData(message.data);
                break;
            case 'error':
                showError(message.message);
                break;
        }
    });

    function handleVectorData(data) {
        loading.style.display = 'none';
        
        if (data.error) {
            showError(data.error);
            return;
        }

        errorDiv.style.display = 'none';
        vectorTable.style.display = 'table';

        // Update header info
        dbType.textContent = `Type: ${data.type.toUpperCase()}`;
        dbCount.textContent = `Count: ${data.count}`;
        dbDimension.textContent = `Dimension: ${data.dimension}`;

        // Store data
        allVectors = data.vectors;
        filteredVectors = [...allVectors];
        currentPage = 1;

        renderTable();
    }

    function handleSearch() {
        const query = searchBox.value.toLowerCase().trim();
        
        if (!query) {
            filteredVectors = [...allVectors];
        } else {
            filteredVectors = allVectors.filter(vector => {
                return vector.id.toLowerCase().includes(query) ||
                       vector.text.toLowerCase().includes(query) ||
                       vector.source.toLowerCase().includes(query);
            });
        }

        currentPage = 1;
        renderTable();
    }

    function handleSort(column) {
        if (sortColumn === column) {
            sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            sortColumn = column;
            sortDirection = 'asc';
        }

        filteredVectors.sort((a, b) => {
            let aVal = a[column] || '';
            let bVal = b[column] || '';

            if (typeof aVal === 'string') {
                aVal = aVal.toLowerCase();
                bVal = bVal.toLowerCase();
            }

            if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
            if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
            return 0;
        });

        // Update sort icons
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.textContent = '↕';
        });

        const activeHeader = document.querySelector(`[data-column="${column}"]`);
        if (activeHeader) {
            const icon = activeHeader.querySelector('.sort-icon');
            icon.textContent = sortDirection === 'asc' ? '↑' : '↓';
        }

        renderTable();
    }

    function renderTable() {
        tableBody.innerHTML = '';

        const totalPages = Math.ceil(filteredVectors.length / itemsPerPage);
        const startIdx = (currentPage - 1) * itemsPerPage;
        const endIdx = Math.min(startIdx + itemsPerPage, filteredVectors.length);
        const pageVectors = filteredVectors.slice(startIdx, endIdx);

        pageVectors.forEach(vector => {
            const row = document.createElement('tr');
            
            // Truncate text for display
            const truncatedText = vector.text.length > 300 
                ? vector.text.substring(0, 300) + '...' 
                : vector.text;

            // Get text length category for color coding
            const lengthClass = getTextLengthClass(vector.text.length);

            // Format vector preview (first 5 dimensions)
            const vectorPreview = vector.vector.slice(0, 5)
                .map(v => v.toFixed(4))
                .join(', ') + '...';

            row.innerHTML = `
                <td class="id-cell">${escapeHtml(vector.id)}</td>
                <td class="text-cell ${lengthClass}" title="Click to see full text">
                    <span class="text-preview">${escapeHtml(truncatedText)}</span>
                    <span class="text-length">(${vector.text.length} chars)</span>
                </td>
                <td class="vector-cell" title="Click to see full vector">
                    <span class="vector-preview">[${vectorPreview}]</span>
                </td>
                <td class="source-cell">${escapeHtml(vector.source)}</td>
            `;

            // Add click handlers
            row.querySelector('.text-cell').addEventListener('click', () => {
                showTextModal(vector);
            });

            row.querySelector('.vector-cell').addEventListener('click', () => {
                showVectorModal(vector);
            });

            tableBody.appendChild(row);
        });

        // Update pagination
        pageInfo.textContent = `Page ${currentPage} of ${totalPages || 1} (${filteredVectors.length} items)`;
        prevPageBtn.disabled = currentPage <= 1;
        nextPageBtn.disabled = currentPage >= totalPages;
    }

    function getTextLengthClass(length) {
        if (length < 100) return 'text-short';
        if (length < 500) return 'text-medium';
        return 'text-long';
    }

    function changePage(delta) {
        currentPage += delta;
        renderTable();
    }

    function showTextModal(vector) {
        modalId.textContent = vector.id;
        modalSource.textContent = vector.source || 'N/A';
        modalLength.textContent = vector.text.length;
        modalText.textContent = vector.text;

        copyTextBtn.onclick = () => copyText(vector.text);

        textModal.style.display = 'flex';
    }

    function showVectorModal(vector) {
        vectorModalId.textContent = vector.id;
        vectorDimensions.textContent = vector.vector.length;
        
        // Format vector for display
        const formattedVector = JSON.stringify(vector.vector, null, 2);
        vectorDisplay.textContent = formattedVector;

        copyVectorBtn.onclick = () => copyVector(vector.vector);

        vectorModal.style.display = 'flex';
    }

    function copyText(text) {
        vscode.postMessage({
            type: 'copyText',
            text: text
        });
    }

    function copyVector(vector) {
        vscode.postMessage({
            type: 'copyVector',
            vector: vector
        });
    }

    function handleRefresh() {
        vscode.postMessage({ type: 'refresh' });
    }

    function handleExport() {
        // Trigger export command
        vscode.postMessage({ type: 'export' });
    }

    function showError(message) {
        loading.style.display = 'none';
        vectorTable.style.display = 'none';
        errorDiv.style.display = 'block';
        errorDiv.textContent = `❌ Error: ${message}`;
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Request initial data
    vscode.postMessage({ type: 'refresh' });
})();
