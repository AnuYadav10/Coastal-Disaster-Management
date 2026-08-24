import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from data.data_service import get_all_locations, get_districts, search_locations, get_stats, get_by_name, get_top_by_population, get_by_district
from data.weather_service import get_weather_for_location, describe_weather, get_condition_icon
from data.charts import get_population_chart_data, get_district_count_data, get_weather_comparison_data
from agent.chat_engine import chat

print('[OK] All imports successful')

locs = get_all_locations()
print('[OK] Locations loaded:', len(locs))

dists = get_districts()
print('[OK] Districts:', len(dists))

stats = get_stats()
print('[OK] Stats cities={} towns={} villages={}'.format(stats['cities'], stats['towns'], stats['villages']))

w = get_weather_for_location('Vapi')
print('[OK] Vapi weather:', w['temperature_c'], 'C,', w['condition'])

w2 = get_weather_for_location('Ahmedabad')
print('[OK] Ahmedabad weather:', w2['temperature_c'], 'C')

s = search_locations('Vapi')
print('[OK] Search Vapi:', [x['name'] for x in s])

top = get_top_by_population(3)
print('[OK] Top 3 by pop:', [x['name'] for x in top])

valsad = get_by_district('Valsad')
print('[OK] Valsad district locations:', len(valsad))

r_weather = chat('What is the weather in Vapi?')
assert 'Vapi' in r_weather, 'Weather response missing Vapi'
print('[OK] Weather chat response length:', len(r_weather))

r_info = chat('Tell me about Surat')
assert 'Surat' in r_info
print('[OK] Info chat OK')

r_list = chat('Show locations in Valsad district')
assert 'Valsad' in r_list
print('[OK] List chat OK')

r_pop = chat('Which city has the highest population?')
assert 'Surat' in r_pop or 'Ahmedabad' in r_pop
print('[OK] Population chat OK')

r_unk = chat('Tell me about Mars colony')
assert len(r_unk) > 10
print('[OK] Unknown location handled OK')

pop_data = get_population_chart_data()
assert len(pop_data['names']) == 20
print('[OK] Population chart data OK:', len(pop_data['names']), 'entries')

dist_data = get_district_count_data()
assert len(dist_data['districts']) > 0
print('[OK] District chart data OK')

wdata = get_weather_comparison_data()
assert len(wdata['temperatures']) == 20
print('[OK] Weather chart data OK')

r_district = chat('Which district does Vapi belong to?')
assert 'Valsad' in r_district
print('[OK] District query chat OK')

r_help = chat('help')
assert 'weather' in r_help.lower()
print('[OK] Help chat OK')

print()
print('=== ALL CHECKS PASSED ===')
