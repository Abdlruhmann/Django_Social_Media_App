document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        // Remove active class from all links
        document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));
        // Add active class to the clicked link
        this.classList.add('active');
        // Hide all content
        document.querySelectorAll('.content').forEach(content => content.classList.remove('active'));
        // Show the target content
        document.getElementById(this.getAttribute('data-target')).classList.add('active');
    });
});