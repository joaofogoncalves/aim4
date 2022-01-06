$(document).ready(function () {
    $('#leaderboard_table').DataTable({
        "order": [[1, "desc"]],
        "pageLength": 50,
    });
    $('.dataTables_length').addClass('bs-select');
});