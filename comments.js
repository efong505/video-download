/**
 * Comments Component
 * Reusable comments system for articles and videos
 * 
 * Usage:
 * <div id="comments-section" data-content-id="article-123" data-content-type="article"></div>
 * <script src="comments.js"></script>
 * <script>initComments();</script>
 */

const COMMENTS_API = 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/comments';

function initComments() {
    const container = document.getElementById('comments-section');
    if (!container) return;
    
    const contentId = container.dataset.contentId;
    const contentType = container.dataset.contentType || 'article';
    
    if (!contentId) {
        console.error('Comments: content-id is required');
        return;
    }
    
    renderCommentsUI(container, contentId, contentType);
    loadComments(contentId);
}

function renderCommentsUI(container, contentId, contentType) {
    const user = getUserData();
    
    container.innerHTML = `
        <div class="comments-container">
            <h3 class="comments-title">
                <i class="fas fa-comments"></i> Comments 
                <span id="comment-count" class="badge bg-primary">0</span>
            </h3>
            
            ${user ? `
                <div class="comment-form-container">
                    <div class="comment-form">
                        <textarea 
                            id="new-comment-text" 
                            class="form-control" 
                            rows="3" 
                            placeholder="Share your thoughts..."
                            maxlength="2000"
                        ></textarea>
                        <div class="comment-form-footer">
                            <small class="text-muted">
                                <span id="char-count">0</span>/2000 characters
                            </small>
                            <button onclick="submitComment('${contentId}', '${contentType}')" class="btn btn-primary btn-sm">
                                <i class="fas fa-paper-plane"></i> Post Comment
                            </button>
                        </div>
                    </div>
                </div>
            ` : `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle"></i> 
                    <a href="login.html">Log in</a> to join the conversation
                </div>
            `}
            
            <div id="comments-list" class="comments-list">
                <div class="text-center py-4">
                    <div class="spinner-border text-primary" role="status"></div>
                    <p class="text-muted mt-2">Loading comments...</p>
                </div>
            </div>
        </div>
    `;
    
    // Character counter
    const textarea = document.getElementById('new-comment-text');
    if (textarea) {
        textarea.addEventListener('input', (e) => {
            document.getElementById('char-count').textContent = e.target.value.length;
        });
    }
}

async function loadComments(contentId) {
    try {
        const response = await fetch(`${COMMENTS_API}?action=get_comments&content_id=${contentId}`);
        const data = await response.json();
        
        const comments = data.comments || [];
        document.getElementById('comment-count').textContent = comments.length;
        
        renderComments(comments);
    } catch (error) {
        console.error('Error loading comments:', error);
        document.getElementById('comments-list').innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i> 
                Failed to load comments. Please try again.
            </div>
        `;
    }
}

function renderComments(comments) {
    const container = document.getElementById('comments-list');
    
    if (comments.length === 0) {
        container.innerHTML = `
            <div class="no-comments text-center py-5">
                <i class="fas fa-comment-slash fa-3x text-muted mb-3"></i>
                <p class="text-muted">No comments yet. Be the first to share your thoughts!</p>
            </div>
        `;
        return;
    }
    
    // Separate parent comments and replies
    const parentComments = comments.filter(c => !c.parent_comment_id);
    const repliesMap = {};
    
    comments.filter(c => c.parent_comment_id).forEach(reply => {
        if (!repliesMap[reply.parent_comment_id]) {
            repliesMap[reply.parent_comment_id] = [];
        }
        repliesMap[reply.parent_comment_id].push(reply);
    });
    
    const html = parentComments.map(comment => {
        const replies = repliesMap[comment.comment_id] || [];
        return renderComment(comment, replies);
    }).join('');
    
    container.innerHTML = html;
}

function renderComment(comment, replies = []) {
    const user = getUserData();
    const isOwner = user && user.email === comment.user_email;
    const isAdmin = user && (user.role === 'admin' || user.role === 'super_user');
    const timeAgo = getTimeAgo(comment.created_at);
    
    const repliesHtml = replies.length > 0 ? `
        <div class="comment-replies">
            ${replies.map(reply => renderComment(reply)).join('')}
        </div>
    ` : '';
    
    return `
        <div class="comment" data-comment-id="${comment.comment_id}">
            <div class="comment-avatar">
                <i class="fas fa-user-circle fa-2x text-secondary"></i>
            </div>
            <div class="comment-content">
                <div class="comment-header">
                    <strong class="comment-author">${escapeHtml(comment.user_name)}</strong>
                    <span class="comment-time text-muted">${timeAgo}</span>
                    ${comment.edited ? '<span class="badge bg-secondary">Edited</span>' : ''}
                </div>
                <div class="comment-text">${escapeHtml(comment.comment_text)}</div>
                <div class="comment-actions">
                    ${user ? `
                        <button onclick="replyToComment('${comment.comment_id}')" class="btn btn-link btn-sm">
                            <i class="fas fa-reply"></i> Reply
                        </button>
                    ` : ''}
                    ${isOwner ? `
                        <button onclick="editComment('${comment.comment_id}')" class="btn btn-link btn-sm text-warning">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button onclick="deleteComment('${comment.content_id}', '${comment.comment_id}')" class="btn btn-link btn-sm text-danger">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    ` : ''}
                    ${isAdmin && !isOwner ? `
                        <button onclick="deleteComment('${comment.content_id}', '${comment.comment_id}', true)" class="btn btn-link btn-sm text-danger">
                            <i class="fas fa-trash"></i> Remove
                        </button>
                    ` : ''}
                </div>
                <div id="reply-form-${comment.comment_id}" class="reply-form" style="display: none;"></div>
            </div>
        </div>
        ${repliesHtml}
    `;
}

async function submitComment(contentId, contentType, parentCommentId = null) {
    const user = getUserData();
    if (!user) {
        alert('Please log in to comment');
        return;
    }
    
    const textarea = document.getElementById(parentCommentId ? `reply-text-${parentCommentId}` : 'new-comment-text');
    const commentText = textarea.value.trim();
    
    if (!commentText) {
        alert('Please enter a comment');
        return;
    }
    
    try {
        const response = await fetch(COMMENTS_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'add_comment',
                content_id: contentId,
                content_type: contentType,
                user_email: user.email,
                user_name: user.first_name || user.email,
                comment_text: commentText,
                parent_comment_id: parentCommentId
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            textarea.value = '';
            if (parentCommentId) {
                document.getElementById(`reply-form-${parentCommentId}`).style.display = 'none';
            }
            loadComments(contentId);
        } else {
            alert(data.error || 'Failed to post comment');
        }
    } catch (error) {
        console.error('Error posting comment:', error);
        alert('Failed to post comment. Please try again.');
    }
}

function replyToComment(commentId) {
    const container = document.getElementById(`reply-form-${commentId}`);
    const user = getUserData();
    
    container.style.display = 'block';
    container.innerHTML = `
        <div class="reply-form-inner mt-2">
            <textarea 
                id="reply-text-${commentId}" 
                class="form-control form-control-sm" 
                rows="2" 
                placeholder="Write a reply..."
                maxlength="2000"
            ></textarea>
            <div class="mt-2">
                <button onclick="submitComment('${container.closest('.comment').dataset.contentId}', 'article', '${commentId}')" class="btn btn-primary btn-sm">
                    <i class="fas fa-paper-plane"></i> Reply
                </button>
                <button onclick="document.getElementById('reply-form-${commentId}').style.display='none'" class="btn btn-secondary btn-sm">
                    Cancel
                </button>
            </div>
        </div>
    `;
}

async function deleteComment(contentId, commentId, isAdmin = false) {
    if (!confirm('Are you sure you want to delete this comment?')) return;
    
    const user = getUserData();
    if (!user) return;
    
    try {
        const response = await fetch(COMMENTS_API, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: 'delete_comment',
                content_id: contentId,
                comment_id: commentId,
                user_email: user.email,
                is_admin: isAdmin
            })
        });
        
        if (response.ok) {
            loadComments(contentId);
        } else {
            alert('Failed to delete comment');
        }
    } catch (error) {
        console.error('Error deleting comment:', error);
        alert('Failed to delete comment');
    }
}

function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

function getTimeAgo(timestamp) {
    const seconds = Math.floor(Date.now() / 1000 - timestamp);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)}d ago`;
    
    return new Date(timestamp * 1000).toLocaleDateString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
