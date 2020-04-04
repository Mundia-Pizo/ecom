    &lt;!DOCTYPE html&gt;
      &lt;html&gt;
      &lt;head&gt;
      &lt;link href=&quot;https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css&quot; type=&quot;text/css&quot; rel=&quot;stylesheet&quot;&gt;
      &lt;style media=&quot;screen&quot;&gt;
     

      &lt;/style&gt;
      &lt;/head&gt;

      &lt;body&gt;
        &lt;div class=&quot;wrapper&quot;&gt;
        &lt;script src=&quot;https://js.stripe.com/v3/&quot;&gt;&lt;/script&gt;

        &lt;form action=&quot;/charge&quot; method=&quot;post&quot; id=&quot;payment-form&quot;&gt;
          &lt;div class=&quot;form-row&quot;&gt;
            &lt;label for=&quot;card-element&quot;&gt;
              Credit or debit card
            &lt;/label&gt;
            &lt;div id=&quot;card-element&quot;&gt;
              &lt;!-- A Stripe Element will be inserted here. --&gt;
            &lt;/div&gt;

            &lt;!-- Used to display form errors. --&gt;
            &lt;div id=&quot;card-errors&quot; role=&quot;alert&quot;&gt;&lt;/div&gt;
          &lt;/div&gt;

          &lt;button&gt;Submit Payment&lt;/button&gt;
        &lt;/form&gt;
        &lt;/div&gt;
        &lt;div id=&quot;stripe-token-handler&quot; class=&quot;is-hidden&quot;&gt;Success! Got token: &lt;span class=&quot;token&quot;&gt;&lt;/span&gt;&lt;/div&gt;
      &lt;/body&gt;

      &lt;script nonce=&quot;AgJ3Rdd8sLhvMdB2LWsdCA==&quot;&gt;  // Create a Stripe client.
        var stripe = Stripe('pk_test_lrMg8UCKes3khZYOTDL5Qj5e000FKtYenf');

        // Create an instance of Elements.
        var elements = stripe.elements();

        // Custom styling can be passed to options when creating an Element.
        // (Note that this demo uses a wider set of styles than the guide below.)
        var style = {
          base: {
            color: '#32325d',
            fontFamily: '&quot;Helvetica Neue&quot;, Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
              color: '#aab7c4'
            }
          },
          invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
          }
        };

        // Create an instance of the card Element.
        var card = elements.create('card', {style: style});

        // Add an instance of the card Element into the `card-element` &lt;div&gt;.
        card.mount('#card-element');

        // Handle real-time validation errors from the card Element.
        card.addEventListener('change', function(event) {
          var displayError = document.getElementById('card-errors');
          if (event.error) {
            displayError.textContent = event.error.message;
          } else {
            displayError.textContent = '';
          }
        });

        // Handle form submission.
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function(event) {
          event.preventDefault();

          stripe.createToken(card).then(function(result) {
            if (result.error) {
              // Inform the user if there was an error.
              var errorElement = document.getElementById('card-errors');
              errorElement.textContent = result.error.message;
            } else {
              // Send the token to your server.
              stripeTokenHandler(result.token);
            }
          });
        });

        // Submit the form with the token ID.
        function stripeTokenHandler(token) {
          // Insert the token ID into the form so it gets submitted to the server
          var form = document.getElementById('payment-form');
          var hiddenInput = document.createElement('input');
          hiddenInput.setAttribute('type', 'hidden');
          hiddenInput.setAttribute('name', 'stripeToken');
          hiddenInput.setAttribute('value', token.id);
          form.appendChild(hiddenInput);

          // Submit the form
          form.submit();
        }

        var successElement = document.getElementById('stripe-token-handler');
        document.querySelector('.wrapper').addEventListener('click', function() {
          successElement.className = 'is-hidden';
        });

        // Not in demo.
        function stripeTokenHandler(token) {
          successElement.className = '';
          successElement.querySelector('.token').textContent = token.id;
        }
      &lt;/script&gt;&lt;/html&gt;