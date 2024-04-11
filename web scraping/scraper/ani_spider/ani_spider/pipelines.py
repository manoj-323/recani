# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import re

class CleanAnimeDataPipeline:
    def process_item(self, item, spider):
        # Clean name_english if available
        if 'name_english' in item and item['name_english'] is not None:
            item['name_english'] = item['name_english'].strip()
        
        # Clean name
        if 'name' in item and item['name'] is not None:
            item['name'] = item['name'].strip()
        
        # Clean score
        if 'score' in item and item['score'] is not None:
            item['score'] = item['score'].strip()
        
        # Clean ranked
        if 'ranked' in item and item['ranked'] is not None:
            item['ranked'] = int((item['ranked'].strip()).replace('#',''))
        
        # Clean popularity
        if 'popularity' in item and item['popularity'] is not None:
            item['popularity'] = int((item['popularity'].strip()).replace('#',''))
        
        # Clean members
        if 'members' in item and item['members'] is not None:
            item['members'] = item['members'].replace(',', '').strip()
        
        # Clean synopsis
        if 'synopsis' in item and item['synopsis'] is not None:
            item['synopsis'] = [re.sub(r'\s+', ' ', syn.strip()) for syn in item['synopsis']]
            item['synopsis'] = " ".join(item['synopsis'])
            item['synopsis'] = item['synopsis'].replace("\"", "")
        
        
        # Clean synonyms
        if 'synonyms' in item and item['synonyms'] is not None:
            item['synonyms'] = item['synonyms'].strip()
        
        # Clean total_episodes
        if 'total_episodes' in item and item['total_episodes'] is not None:
            item['total_episodes'] = re.sub(r'\s+', ' ', item['total_episodes'].strip())
        
        # Clean premiered
        if 'premiered' in item and item['premiered'] is not None:
            item['premiered'] = item['premiered'].strip()
        
        # Clean studios
        if 'studios' in item and item['studios'] is not None:
            item['studios'] = item['studios'].strip()
        
        # Clean genres
        if 'genres' in item and item['genres'] is not None:
            item['genres'] = [genre.strip() for genre in item['genres']]
        
        # Clean demographic
        if 'demographic' in item and item['demographic'] is not None:
            item['demographic'] = item['demographic'].strip()
        
        # Clean duration_per_ep
        if 'duration_per_ep' in item and item['duration_per_ep'] is not None:
            item['duration_per_ep'] = re.sub(r'\s+', ' ', item['duration_per_ep'].strip())
        
        # Clean rating
        if 'rating' in item and item['rating'] is not None:
            item['rating'] = item['rating'].strip()
        
        # Clean scored_by
        if 'scored_by' in item and item['scored_by'] is not None:
            item['scored_by'] = item['scored_by'].strip()
        
        # Clean favorites
        if 'favorites' in item and item['favorites'] is not None:
            item['favorites'] = item['favorites'].replace(',', '').strip()
        
        # Clean aired
        if 'aired' in item and item['aired'] is not None:
            item['aired'] = re.sub(r'\s+', ' ', item['aired'].strip())
        
        # Clean source
        if 'source' in item and item['source'] is not None:
            item['source'] = item['source'].strip()
        
        # Clean watching
        if 'watching' in item and item['watching'] is not None:
            item['watching'] = item['watching'].strip()
        
        # Clean completed
        if 'completed' in item and item['completed'] is not None:
            item['completed'] = item['completed'].strip()
        
        # Clean on_hold
        if 'on_hold' in item and item['on_hold'] is not None:
            item['on_hold'] = item['on_hold'].strip()
        
        # Clean dropped
        if 'dropped' in item and item['dropped'] is not None:
            item['dropped'] = item['dropped'].strip()
        
        # Clean plan_to_watch
        if 'plan_to_watch' in item and item['plan_to_watch'] is not None:
            item['plan_to_watch'] = item['plan_to_watch'].strip()
        
        # Clean total
        if 'total' in item and item['total'] is not None:
            item['total'] = item['total'].strip()

        # clean votes (scored_(x)_by)
        for i in range(10, 0, -1):
            key = f'scored_{i}_by'
            if key in item and item[key] is not None:
                # Extract numerical data
                numerical_data = re.findall(r'\((\d+)\s+votes\)', item[key])
                if numerical_data:
                    item[key] = numerical_data[0]
                else:
                    item[key] = None
                
        return item