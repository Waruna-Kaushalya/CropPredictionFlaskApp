$(document).ready(function () {
  $('#containerForm').bootstrapValidator({
    container: 'tooltip',
    feedbackIcons: {
      valid: 'glyphicon glyphicon-ok',
      invalid: 'glyphicon glyphicon-remove',
      validating: 'glyphicon glyphicon-refresh'
    },
    fields: {

      Rainfall: {
        validators: {
          numeric: {
            message: 'Please enter numeric values only'
          },
          notEmpty: {
            message: '* Field is required'
          }
        }
      },

      MaximumTemperature: {
        validators: {
          numeric: {
            message: 'Please enter numeric values only'
          },
          notEmpty: {
            message: '* Field is required'
          }
        }
      },

      MinimumTemperature: {
        validators: {
          numeric: {
            message: 'Please enter numeric values only'
          },
          notEmpty: {
            message: '* Field is required'
          }
        }
      },

      RelativeHumidity: {
        validators: {
          numeric: {
            message: 'Please enter numeric values only'
          },
          notEmpty: {
            message: '* Field is required'
          }
        }
      },

      Pressure: {
        validators: {
          numeric: {
            message: 'Please enter numeric values only'
          },
          notEmpty: {
            message: '* Field is required'
          }
        }
      }
    }
  });
});

