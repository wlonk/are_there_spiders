/* Project specific Javascript goes here. */

function toggle_season_and_episode () {
  if ($('#id_artwork_kind').val() === 'show') {
    $('#artwork_season_control_group').show();
    $('#artwork_episode_control_group').show();
  } else {
    $('#artwork_season_control_group').hide();
    $('#artwork_episode_control_group').hide();
  }
}

$(document).ready(function () {
  toggle_season_and_episode();
  $('#id_artwork_kind').change(toggle_season_and_episode);
});
