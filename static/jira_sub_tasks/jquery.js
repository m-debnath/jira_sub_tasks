$(function () {
    $(document).ready(function(){
        $('[data-toggle="tooltip"]').tooltip();
        $(document).on('shown.bs.tooltip', function (e) {
          setTimeout(function () {
            $(e.target).tooltip('hide');
          }, 2500);
        });
        $('#id_dev_int_deploy').datetimepicker({
            format: 'YYYY-MM-DD',
            daysOfWeekDisabled: [0, 6],
            minDate: moment()
        });
        $('#id_dev_uat_deploy').datetimepicker({
            format: 'YYYY-MM-DD',
            daysOfWeekDisabled: [0, 6],
            minDate: moment()
        });
        $('#id_ana_due_dt').datetimepicker({
            format: 'YYYY-MM-DD',
            daysOfWeekDisabled: [0, 6],
            minDate: moment()
        });
        $("#id_proceed_checkbox").click(function() {
            $("#id_btn_proceed").attr("disabled", !this.checked);
        });
        $("#id_dev_assign").on('change', function() {
            if ($("#id_dev_assign").val() != '') {
                $("#id_dev_assign").removeClass("border-danger").addClass("border-success");
                $("#id_dev_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_dev_assign").removeClass("border-success").addClass("border-danger");
                $("#id_dev_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
        $('#id_test_assign').on('change', function() {
            $('#id_test_auto_assign').val(this.value);
            $('.selectpicker').selectpicker('refresh');
            if ($("#id_test_assign").val() != '') {
                $("#id_test_assign").removeClass("border-danger").addClass("border-success");
                $("#id_test_assign").parent().removeClass("border-danger").addClass("border-success");
                $("#id_test_auto_assign").removeClass("border-danger").addClass("border-success");
                $("#id_test_auto_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_test_assign").removeClass("border-success").addClass("border-danger");
                $("#id_test_assign").parent().removeClass("border-success").addClass("border-danger");
                $("#id_test_auto_assign").removeClass("border-success").addClass("border-danger");
                $("#id_test_auto_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
        $("#id_ana_assign").on('change', function() {
            if ($("#id_ana_assign").val() != '') {
                $("#id_ana_assign").removeClass("border-danger").addClass("border-success");
                $("#id_ana_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_ana_assign").removeClass("border-success").addClass("border-danger");
                $("#id_ana_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
        $("#id_test_auto_assign").on('change', function() {
            if ($("#id_test_auto_assign").val() != '') {
                $("#id_test_auto_assign").removeClass("border-danger").addClass("border-success");
                $("#id_test_auto_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_test_auto_assign").removeClass("border-success").addClass("border-danger");
                $("#id_test_auto_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
        $("#id_dev_rvw_assign").on('change', function() {
            if ($("#id_dev_rvw_assign").val() != '') {
                $("#id_dev_rvw_assign").removeClass("border-danger").addClass("border-success");
                $("#id_dev_rvw_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_dev_rvw_assign").removeClass("border-success").addClass("border-danger");
                $("#id_dev_rvw_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
        $("#id_condev_rvw_assign").on('change', function() {
            if ($("#id_condev_rvw_assign").val() != '') {
                $("#id_condev_rvw_assign").removeClass("border-danger").addClass("border-success");
                $("#id_condev_rvw_assign").parent().removeClass("border-danger").addClass("border-success");
            } else {
                $("#id_condev_rvw_assign").removeClass("border-success").addClass("border-danger");
                $("#id_condev_rvw_assign").parent().removeClass("border-success").addClass("border-danger");
            }
        });
    });
});