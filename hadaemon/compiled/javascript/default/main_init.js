$(function(){ //DOM Ready

    function navigate(url)
    {
        window.location.href = url;
    }

    $(document).attr("title", "Main Panel");
    content_width = (120 + 5) * 10 + 5
    $('.gridster').width(content_width)
    $(".gridster ul").gridster({
        widget_margins: [5, 5],
        widget_base_dimensions: [120, 120],
        avoid_overlapped_widgets: true,
        max_rows: 15,
        max_size_x: 10,
        shift_widgets_up: false
    }).data('gridster').disable();
    
    // Add Widgets

    var gridster = $(".gridster ul").gridster().data('gridster');
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseclock-default-clock" id="default-clock"><h1 class="date"data-bind="text: date, attr: {style: date_style}"></h1><h2 class="time" data-bind="text: time, attr: {style: time_style}"></h2></div></li>', 2, 1, 1, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baseweather-default-weather" id="default-weather"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><div data-bind="attr: {style: main_style}"><p class="primary-climacon" data-bind="css: icon"></p><p class="primary-info" data-bind="text: temperature"></p><p class="primary-unit" data-bind="html: unit, attr: {style: unit_style}"></p><br></div><div data-bind="attr: {style: sub_style}"><p class="secondary-detail" data-bind="visible: apparent_temperature"><span class="secondary-icon mdi mdi-thermometer-lines" title="Apparent Temp" data-bind="visible: prefer_icons"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Apparent Temp:&nbsp;</span><span class="secondary-info" data-bind="html: apparent_temperature"></span><span class="secondary-info" data-bind="html: unit, attr: {style: sub_unit_style}"></span></p><p class="secondary-detail" data-bind="visible: humidity"><span class="secondary-icon mdi mdi-water-percent" title="Humidity" data-bind="visible: prefer_icons"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Humidity:&nbsp;</span><span class="secondary-info" data-bind="text: humidity"></span><span class="secondary-unit" data-bind="attr: {style: sub_unit_style}">%</span><br></p><p class="secondary-detail"  data-bind="visible: precip_probability() || precip_intensity()"><span data-bind="visible: precip_probability"><span class="secondary-icon mdi" title="Rain" data-bind="visible: prefer_icons, css: precip_type_icon"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Rain:&nbsp;</span><span class="secondary-info" data-bind="text: precip_probability"></span><span class="secondary-unit" data-bind="attr: {style: sub_unit_style}">%</span></span><span data-bind="visible: precip_intensity"><span class="secondary-info" data-bind="visible: precip_intensity() && precip_probability()">&nbsp;/&nbsp;</span><span class="secondary-info" data-bind="text: precip_intensity"></span><span class="secondary-unit" data-bind="text: rain_unit, attr: {style: sub_unit_style}"></span></span></p><p class="secondary-detail" data-bind="visible: wind_speed"><span class="secondary-icon mdi mdi-weather-windy" data-bind="visible: prefer_icons, css: bearing_icon, attr: {title: wind_bearing() + \'&deg;\'}"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Wind:&nbsp;</span><span class="secondary-info" data-bind="text: wind_speed"></span><span class="secondary-unit" data-bind="text: wind_unit, attr: {style: sub_unit_style}"></span></p><p class="secondary-detail" data-bind="visible: wind_bearing() && !prefer_icons()"><span class="secondary-info" data-bind="html: wind_bearing"></span><span class="secondary-unit" data-bind="attr: {style: sub_unit_style}">&deg;</span></p><p class="secondary-detail" data-bind="visible: pressure() != \'\'"><span class="secondary-icon mdi mdi-gauge" data-bind="visible: prefer_icons"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Pressure:&nbsp;</span><span class="secondary-info" data-bind="text: pressure"></span><span class="secondary-info" data-bind="text: pressure_unit, attr: {style: sub_unit_style}"></span></p><div data-bind="visible: show_forecast"> <hr><h1 class="title" data-bind="text: forecast_title, attr:{ style: title_style}, visible: show_forecast"></h1><p class="secondary-detail" data-bind="visible: forecast_temperature_min"><span class="secondary-climacon" data-bind="css: forecast_icon"></span></p><p class="secondary-detail" data-bind="visible: forecast_temperature_min"><span class="secondary-info" data-bind="text: forecast_temperature_min"></span><span class="secondary-info" data-bind="visible: forecast_temperature_max"><span>/</span><span class="secondary-info" data-bind="text: forecast_temperature_max"></span></span></p><p class="secondary-detail" data-bind="visible: forecast_precip_probability"><span class="secondary-icon mdi" title="Rain" data-bind="visible: prefer_icons, css: forecast_precip_type_icon"></span><span class="secondary-info" data-bind="visible: !prefer_icons()">Rain:&nbsp;</span><span class="secondary-info" data-bind="text: forecast_precip_probability"></span><span class="secondary-icon" data-bind="attr: {style: sub_unit_style}">%</span></p></div></div></div></li>', 2, 2, 3, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-side-temperature" id="default-side-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 5, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-side-humidity" id="default-side-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 6, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-mode" id="default-mode"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 2, 1, 7, 1)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-baselight-default-light-office-gateway-light" id="default-light-office-gateway-light"><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2><span class="toggle-area" id="switch"></span><p class="state_text" data-bind="text: state_text, attr:{style: state_text_style}"></p><div class="levelunit"><p class="level" data-bind="text: level, attr:{style: level_style}"></p><p class="unit" data-bind="html: units, attr:{style: unit_style}"></p></div><p class="secondary-icon minus"><i data-bind="attr: {class: icon_down, style: level_down_style}" id="level-down"></i></p><p class="secondary-icon plus"><i data-bind="attr: {class: icon_up, style: level_up_style}" id="level-up"></i></p></div></li>', 1, 1, 1, 3)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-kids-temperature" id="default-sensor-kids-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 4)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-bedroom-temperature" id="default-sensor-bedroom-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 4)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-office-temperature" id="default-sensor-office-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 3, 4)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-bathroom-temperature" id="default-sensor-bathroom-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 4, 4)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-kitchen-temperature" id="default-sensor-kitchen-temperature"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 5, 4)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-kids-humidity" id="default-sensor-kids-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 1, 5)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-bedroom-humidity" id="default-sensor-bedroom-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 2, 5)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-office-humidity" id="default-sensor-office-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 3, 5)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-bathroom-humidity" id="default-sensor-bathroom-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 4, 5)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basedisplay-default-sensor-kitchen-humidity" id="default-sensor-kitchen-humidity"><h1 class="title" data-bind="text: title, attr:{ style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{ style: title2_style}"></h1><div class="valueunit" data-bind="attr:{ style: container_style}"><h2 class="value" data-bind="html: value, attr:{ style: value_style}"></h2><p class="unit" data-bind="html: unit, attr:{ style: unit_style}"></p></div><h1 class="state_text" data-bind="text: state_text, attr: {style: state_text_style}"></h1></div></li>', 1, 1, 5, 5)
    
        gridster.add_widget('<li><div data-bind="attr: {style: widget_style}" class="widget widget-basejavascript-default-reload" id="default-reload"><span class="toggle-area" id="switch"></span><h1 class="title" data-bind="text: title, attr:{style: title_style}"></h1><h1 class="title2" data-bind="text: title2, attr:{style: title2_style}"></h1><h2 class="icon" data-bind="attr:{style: icon_style}"><i data-bind="attr: {class: icon}"></i></h2></div></li>', 1, 1, 1, 6)
    
    
    
    var widgets = {}
    // Initialize Widgets
    
        widgets["default-clock"] = new baseclock("default-clock", "", "default", {'widget_type': 'baseclock', 'use_comma': 0, 'date_style': 'color: white;', 'time_style': 'color: cyan;', 'time_format': '24hr', 'icons': [], 'precision': 1, 'namespace': 'default', 'date_format_country': 'pl', 'static_icons': [], 'fields': {'time': '', 'date': ''}, 'use_hass_icon': 1, 'show_seconds': 1, 'css': {}, 'static_css': {'time_style': 'color: cyan;', 'widget_style': 'background-color: #444;', 'date_style': 'color: white;'}})
    
        widgets["default-weather"] = new baseweather("default-weather", "", "default", {'widget_type': 'baseweather', 'use_comma': 0, 'static_css': {'widget_style': 'background-color: #444;', 'unit_style': 'color: #ffaa00;', 'sub_style': 'color: #00aaff;', 'title_style': 'color: #00aaff;', 'main_style': 'color: #ffaa00;', 'sub_unit_style': 'color: #00aaff;'}, 'icons': {'sleet': 'mdi-weather-snowy-rainy', 'unknown': 'mdi-umbrella', 'rain': 'mdi-umbrella', 'snow': 'mdi-snowflake'}, 'units': '&deg;C', 'precision': 1, 'namespace': 'default', 'static_icons': [], 'fields': {'icon': '', 'pressure': '', 'forecast_precip_type_icon': 'mdi-umbrella', 'precip_probability': '', 'forecast_precip_type': '', 'forecast_icon': '', 'bearing_icon': 'mdi-rotate-0', 'humidity': '', 'wind_speed': '', 'apparent_temperature': '', 'temperature': '', 'rain_unit': '', 'forecast_precip_probability': '', 'precip_type': '', 'precip_type_icon': 'mdi-umbrella', 'prefer_icons': 0, 'precip_intensity': '', 'title': '', 'wind_unit': '', 'pressure_unit': '', 'show_forecast': 0, 'forecast_temperature_min': '', 'forecast_temperature_max': '', 'wind_bearing': '', 'forecast_title': '', 'unit': ''}, 'use_hass_icon': 1, 'css': {}, 'entities': {'forecast_precip_probability': 'sensor.dark_sky_precip_probability_1', 'icon': 'sensor.dark_sky_icon', 'pressure': 'sensor.dark_sky_pressure', 'precip_probability': 'sensor.dark_sky_precip_probability', 'forecast_precip_type': 'sensor.dark_sky_precip_1', 'forecast_icon': 'sensor.dark_sky_icon_1', 'precip_intensity': 'sensor.dark_sky_precip_intensity', 'humidity': 'sensor.dark_sky_humidity', 'precip_type': 'sensor.dark_sky_precip', 'apparent_temperature': 'sensor.dark_sky_apparent_temperature', 'temperature': 'sensor.dark_sky_temperature', 'forecast_temperature_min': 'sensor.dark_sky_daily_low_temperature_1', 'forecast_temperature_max': 'sensor.dark_sky_daily_high_temperature_1', 'wind_speed': 'sensor.dark_sky_wind_speed', 'wind_bearing': 'sensor.dark_sky_wind_bearing'}})
    
        widgets["default-side-temperature"] = new basedisplay("default-side-temperature", "", "default", {'widget_type': 'basedisplay', 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'units': '&deg;F', 'sub_entity_to_entity_attribute': '', 'precision': 0, 'namespace': 'default', 'entity': 'sensor.side_temp_corrected', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': 'Temperature'}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-side-humidity"] = new basedisplay("default-side-humidity", "", "default", {'widget_type': 'basedisplay', 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'units': '%', 'sub_entity_to_entity_attribute': '', 'precision': 0, 'namespace': 'default', 'entity': 'sensor.side_humidity_corrected', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': 'Humidity'}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-mode"] = new basedisplay("default-mode", "", "default", {'widget_type': 'basedisplay', 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'input_select.house_mode', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': 'House Mode'}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-light-office-gateway-light"] = new baselight("default-light-office-gateway-light", "", "default", {'widget_type': 'baselight', 'title_is_friendly_name': 1, 'post_service_active': {'entity_id': 'light.corridor_gateway_light', 'service': 'homeassistant/turn_on'}, 'post_service_inactive': {'entity_id': 'light.corridor_gateway_light', 'service': 'homeassistant/turn_off'}, 'use_comma': 0, 'static_css': {'state_text_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'level_style': 'color: #fff;', 'title_style': 'color: #fff;', 'level_up_style': 'color: #888;', 'unit_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'level_down_style': 'color: #888;'}, 'icons': {'icon_on': 'fa-circle', 'icon_off': 'fa-circle-thin'}, 'precision': 1, 'namespace': 'default', 'entity': 'light.corridor_gateway_light', 'static_icons': {'icon_up': 'fa-plus', 'icon_down': 'fa-minus'}, 'fields': {'state_text': '', 'level': '', 'title2': '', 'title': '', 'units': '%', 'icon': '', 'icon_style': ''}, 'use_hass_icon': 1, 'css': {'icon_style_active': 'color: #aaff00;', 'icon_style_inactive': 'color: #888;'}})
    
        widgets["default-sensor-kids-temperature"] = new basedisplay("default-sensor-kids-temperature", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.kids_temperature', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-bedroom-temperature"] = new basedisplay("default-sensor-bedroom-temperature", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.bedroom_temperature', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-office-temperature"] = new basedisplay("default-sensor-office-temperature", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.office_temperature', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-bathroom-temperature"] = new basedisplay("default-sensor-bathroom-temperature", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.bathroom_temperature', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-kitchen-temperature"] = new basedisplay("default-sensor-kitchen-temperature", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.kitchen_temperature', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-kids-humidity"] = new basedisplay("default-sensor-kids-humidity", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.kids_humidity', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-bedroom-humidity"] = new basedisplay("default-sensor-bedroom-humidity", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.bedroom_humidity', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-office-humidity"] = new basedisplay("default-sensor-office-humidity", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.office_humidity', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-bathroom-humidity"] = new basedisplay("default-sensor-bathroom-humidity", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.bathroom_humidity', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-sensor-kitchen-humidity"] = new basedisplay("default-sensor-kitchen-humidity", "", "default", {'widget_type': 'basedisplay', 'title_is_friendly_name': 1, 'entity_to_sub_entity_attribute': '', 'use_comma': 0, 'static_css': {'title_style': 'color: #fff;', 'widget_style': 'background-color: #444;', 'title2_style': 'color: #fff;', 'container_style': '', 'state_text_style': 'font-size: 100%;color: #fff;'}, 'sub_entity': '', 'icons': [], 'sub_entity_to_entity_attribute': '', 'precision': 1, 'namespace': 'default', 'entity': 'sensor.kitchen_humidity', 'static_icons': [], 'fields': {'state_text': '', 'unit': '', 'title2': '', 'value': '', 'title': ''}, 'use_hass_icon': 1, 'css': {'value_style': 'font-size: 250%;color: #00aaff;', 'text_style': 'font-size: 100%;color: #fff;', 'unit_style': 'font-size: 100%;color: #00aaff;'}})
    
        widgets["default-reload"] = new basejavascript("default-reload", "", "default", {'widget_type': 'basejavascript', 'static_css': {'title_style': 'color: #fff;', 'title2_style': 'color: #fff;', 'widget_style': 'background-color: #444;'}, 'namespace': 'default', 'use_comma': 0, 'static_icons': [], 'fields': {'title2': '', 'title': '', 'icon': '', 'icon_style': ''}, 'use_hass_icon': 1, 'css': {'icon_inactive_style': 'color: #fff;', 'icon_active_style': 'color: #fff;'}, 'icons': {'icon_active': 'fa-spinner fa-spin', 'icon_inactive': 'fa-refresh'}, 'precision': 1, 'command': 'location.reload(true)'})
    

    // Setup click handler to cancel timeout navigations

    $( ".gridster" ).click(function(){
        clearTimeout(myTimeout);
        if (myTimeoutSticky) {
            myTimeout = setTimeout(function() { navigate(myTimeoutUrl); }, myTimeoutDelay);
        }
    });

    // Set up timeout

    var myTimeout;
    var myTimeoutUrl;
    var myTimeoutDelay;
    var myTimeoutSticky = 0;

    if (location.search != "")
    {
        var query = location.search.substr(1);
        var result = {};
        query.split("&").forEach(function(part) {
        var item = part.split("=");
        result[item[0]] = decodeURIComponent(item[1]);
        });

        if ("timeout" in result && "return" in result)
        {
            url = result.return
            argcount = 0
            for (arg in result)
            {
                if (arg != "timeout" && arg != "return" && arg != "sticky")
                {
                    if (argcount == 0)
                    {
                        url += "?";
                    }
                    else
                    {
                        url += "?";
                    }
                    argcount ++;
                    url += arg + "=" + result[arg]
                }
            }
            if ("sticky" in result)
            {
                myTimeoutSticky = (result.sticky == "1");
            }
            myTimeoutUrl = url;
            myTimeoutDelay = result.timeout * 1000;
            myTimeout = setTimeout(function() { navigate(url); }, result.timeout * 1000);
        }
    }

    // Start listening for HA Events
    if (location.protocol == 'https:')
    {
        wsprot = "wss:"
    }
    else
    {
        wsprot = "ws:"
    }
    var stream_url = wsprot + '//' + location.host + '/stream'
    ha_status(stream_url, "Main Panel", widgets);

});