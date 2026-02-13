// Replace the uploadImageToS3 function in create-article.html with this:

function uploadImageToS3(file) {
    var reader = new FileReader();
    
    reader.onload = function(e) {
        // Get base64 data (remove data:image/...;base64, prefix)
        var base64Data = e.target.result.split(',')[1];
        var fileExt = file.name.split('.').pop().toLowerCase();
        
        // Send as JSON instead of FormData
        fetch(ADMIN_API + '?action=upload_image', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + authToken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_data: base64Data,
                file_ext: fileExt
            })
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            if (data.url) {
                document.getElementById('featured-image-url').value = data.url;
                showFeaturedImagePreview(data.url);
                alert('Image uploaded to S3 successfully!');
            } else {
                alert('Error uploading image: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(function(error) {
            console.error('Upload error:', error);
            alert('Failed to upload image');
        });
    };
    
    reader.readAsDataURL(file);
}
