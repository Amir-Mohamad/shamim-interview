from django import forms


class AddPaymentForm(forms.Form):

    title = forms.CharField(max_length=250)
    date = forms.CharField(max_length=250)
    employee_count = forms.IntegerField()

    def __init__(self, *args, **kwargs):

        extra_fields = kwargs.pop('extra', 0)

        # check if extra_fields exist. If they don't exist assign 0 to them
        if not extra_fields:
            extra_fields = 0

        super(AddPaymentForm, self).__init__(*args, **kwargs)

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['employee_name_field_{index}'.format(
                index=index)] = forms.CharField()
            self.fields['hour_field_{index}'.format(
                index=index)] = forms.IntegerField()
            self.fields['price_field_{index}'.format(
                index=index)] = forms.IntegerField()
