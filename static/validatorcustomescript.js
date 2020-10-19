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

          between: {
            min: 0,
            max: 100,
            message: 'The number must be between 0 and 100'
          },

          numeric: {
            message: 'Please enter numeric values only'
          },

          notEmpty: {
            message: '* Field is required'
          },

          
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

