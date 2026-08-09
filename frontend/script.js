document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('document-file');
    const accessLevel = document.getElementById('access-level').value;
    
    if (fileInput.files.length === 0) return;
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('access_level', accessLevel);
    
    document.getElementById('upload-status').innerText = 'Uploading...';
    
    try {
        const response = await fetch('/api/documents/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        document.getElementById('upload-status').innerHTML = `
            <p>Document: ${result.filename}</p>
            <p>Status: ${result.status}</p>
            <p>Chunks: ${result.chunks}</p>
            <p>Access: ${accessLevel}</p>
        `;
    } catch (err) {
        document.getElementById('upload-status').innerText = 'Upload failed.';
    }
});

document.getElementById('ask-btn').addEventListener('click', async () => {
    const query = document.getElementById('query-input').value;
    const userRole = document.getElementById('user-role').value;
    if (!query) return;
    
    document.getElementById('results-container').style.display = 'block';
    document.getElementById('ai-content').innerText = 'Loading...';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, user_role: userRole })
        });
        const result = await response.json();
        
        // Security
        const sec = result.security;
        document.getElementById('security-content').innerHTML = `
            <p>Risk Score: ${sec.risk_score}/100</p>
            <p>Risk Level: ${sec.risk_level}</p>
            <p>Decision: <strong>${sec.decision}</strong></p>
        `;
        
        // Retrieval
        const ret = result.retrieval;
        let retHtml = \`<p>Documents Retrieved: \${ret.documents}</p>\`;
        ret.sources.forEach(s => {
            retHtml += \`<p>\${s.filename} - Relevance: \${s.relevance}%</p>\`;
        });
        document.getElementById('retrieval-content').innerHTML = retHtml;
        
        // Tokens
        const tok = result.tokens;
        document.getElementById('token-content').innerHTML = `
            <div class="flex-row"><span>Original: ${tok.original}</span> <span>Optimized: ${tok.optimized}</span></div>
            <div class="flex-row"><span>Saved: ${tok.saved}</span> <span>Reduction: ${tok.reduction}%</span></div>
            <small>(Estimated Token Usage)</small>
        `;
        
        // AI Response
        document.getElementById('ai-content').innerHTML = \`<p>\${result.answer}</p>\`;
        
        // Sources
        let srcHtml = '';
        ret.sources.forEach((s, idx) => {
            srcHtml += \`<p>\${idx + 1}. \${s.filename} (Relevance: \${s.relevance}%)</p>\`;
        });
        document.getElementById('sources-content').innerHTML = srcHtml || '<p>No sources.</p>';
        
    } catch (err) {
        document.getElementById('ai-content').innerText = 'Error processing request.';
    }
});
