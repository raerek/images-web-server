<!DOCTYPE html>
<html lang="hu" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Page served from {{hostname}}.</title>
  </head>
  <body>
    % for image in images:
      <img src="/images/{{image}}" alt="">
    % end
  </body>
</html>
