def categorize_weather(cond):
    """
    Convertier variaciones de categories de clima a una categoria unificada
    """
    cond = str(cond).lower()

    if any(x in cond for x in ['snow', 'sleet', 'ice', 'blizzard', 'hail', 'wintry mix']):
        return 'Snowy'
    elif any(x in cond for x in ['rain', 'drizzle', 'shower', 'thunder']):
        return 'Rainy'
    elif any(x in cond for x in ['cloud', 'overcast', 'fog', 'haze', 'mist', 'smoke', 'partial fog', 'pockets of fog']):
        return 'Cloudy'
    elif any(x in cond for x in ['fair', 'clear', 'sunny']):
        return 'Fair'
    elif any(x in cond for x in ['dust', 'sand', 'volcanic ash', 'duststorm', 'dust whirls']):
        return 'Dusty'
    elif 'wind' in cond:
        return 'Windy'
    elif any(x in cond for x in ['tornado', 'funnel cloud']):
        return 'Extreme'
    else:
        return 'Other'