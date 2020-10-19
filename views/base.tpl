<!DOCTYPE html>
<html lang="hu" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Page served from {{hostname}}.</title>
  </head>
  <body>
    % if images:
      % for image in images:
        <img src="/images/{{image}}" alt="">
      % end
    % end
    % if error_message:
      {{error_message}}
    % end
  </body>
</html>
