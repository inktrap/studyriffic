<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{title or 'No title'}}</title>
    <link rel="stylesheet" href="{{url('static', filepath='base.css')}}">
    <link rel="stylesheet" href="{{url('static', filepath='bootstrap/css/bootstrap.min.css')}}">
    % if defined('css'):
        % for c in css:
            <link rel="stylesheet" href="{{url('static', filepath=c)}}">
        % end
    % end
    <!-- favicon made with  https://realfavicongenerator.net -->
    <!-- favicon license: CC0 Public Comain. Source: https://pixabay.com/en/chart-graph-graphic-statistics-35773/ -->
    <link rel="apple-touch-icon" sizes="180x180" href="{{url('static', filepath='icons/apple-touch-icon.png')}}">
    <link rel="icon" type="image/png" href="{{url('static', filepath='icons/favicon-32x32.png" sizes="32x32')}}">
    <link rel="icon" type="image/png" href="{{url('static', filepath='icons/favicon-16x16.png" sizes="16x16')}}">
    <link rel="manifest" href="{{url('static', filepath='icons/manifest.json')}}">
    <link rel="mask-icon" href="{{url('static', filepath='icons/safari-pinned-tab.svg" color="#5bbad5')}}">
    <link rel="shortcut icon" href="{{url('static', filepath='icons/favicon.ico')}}">
    <meta name="msapplication-config" content="{{url('static', filepath='icons/browserconfig.xml')}}">
    <meta name="theme-color" content="#ffffff">

    <noscript>
        JavaScript is not available but is required for this study to work!
        <style type="text/css">
            #main { display:none; }
        </style>
    </noscript>

    <script src="{{url('static', filepath='jquery.js')}}"></script>
  </head>
  <body>
    <div id="main" class="container">
        <div class="row">
        <!--
         col-xs-10 col-xs-offset-1
         -->
            <div id="content"
                        class="col-md-6 col-md-offset-3
                        col-lg-6 col-lg-offset-3">
            {{!base}}
            </div>
        </div>
    </div>
    <script type="text/javascript"> 
       var task_url = "{{url('task', study=study)}}";
       var demographics_url = "{{url('demographics', study=study)}}";
       var demographics_complete_url = "{{url('demographics-complete', study=study)}}";
       var last_url = "{{url('last', study=study)}}";
    </script>
    % if defined('js'):
        % for j in js:
            <script src="{{url('static', filepath=j)}}"></script>
        % end
    % end
  </body>


</html>
