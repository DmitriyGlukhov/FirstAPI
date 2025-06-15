from typing import Optional, List
import os
import csv
import uuid
import time
import json

class DBEngine:
    engine: Optional['DBEngine'] = None
    
    cookies_fields = ['cookie', 'user_id', 'expire']
    
    
    @classmethod
    def create_engine(cls, *args, **kwargs) -> 'DBEngine':
        if cls.engine is not None:
            ValueError('')
        
        cls.engine = cls(*args, **kwargs)
        return cls.engine
    
    @classmethod
    def get_engine(cls) -> 'DBEngine':
        if cls.engine is None:
            raise ValueError('Движок не проинициализирован')
        return cls.engine
    
    
    def __init__(self, path: str):
        if self.engine is not None:
            raise ValueError()
        
        self.cookies_file = os.path.join(path, 'cookies.csv')
        self.user_dir = os.path.join(path, 'user')
        self.task_dir = os.path.join(path, 'task')
        
    @staticmethod
    def get_free_id(dir: str):
        ids = [name[:name.find('.')] for name in os.listdir(dir)]
        if not ids:
            return 1
        return int(sorted(ids)[-1]) + 1
    
    def create_cookie(self, user_id: int, expire:float) -> str:
        with open(self.cookies_file, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.cookies_fields)
            
            cookie = str(uuid.uuid4())
            writer.writerow({
                'cookie': cookie,
                'user_id': user_id,
                'expire': int(expire)
            })
        return cookie
    
    def remove_cookie(self, user_id, cookie):
        with open(self.cookies_file, 'r') as f:
            reader = csv.DictReader(f, fieldnames=self.cookies_fields)
            rows = [
                row for row in reader 
                if not (row['cookie'] == cookie and row['user_id'] == str(user_id))
            ]
        print(rows)
        with open (self.cookies_file, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.cookies_fields)
            writer.writerows(rows)
        
    
    def get_user_id_by_cookie(self, cookie) -> Optional[int]:
        t = time.time()
        with open(self.cookies_file, 'r') as f:
            reader = csv.DictReader(f, fieldnames=self.cookies_fields)
            for row in reader:
                if row['cookie'] == cookie and t <= int(row['expire']):
                    return int(row['user_id'])
        return None
    
    
    def get_user_data(self, user_id: int) -> Optional[dict]:
        filename = os.path.join(self.user_dir, f"{user_id}.json")
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
        
    def find_one_user(self, **kwargs) -> Optional[dict]:
        for filename in os.listdir(self.user_dir):
            user_id = int(filename[:filename.find('.')])
            data = self.get_user_data(user_id)
            if all([data.get(k) == v for k, v in kwargs.items()]):
                return data
        
    def find_users(self, **kwargs) -> List[dict]:
        result = []
        for filename in os.listdir(self.user_dir):
            user_id = int(filename[:filename.find('.')])
            data = self.get_user_data(user_id)
            if all([data.get(k) == v for k, v in kwargs.items()]):
                result.append(data)
        return result
        
    def update_user(self, user_id: int, **data):
        filename = os.path.join(self.user_dir, f"{user_id}.json")
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=True)
            
    def create_user(self, **data):
        new_id = self.get_free_id(self.user_dir)
        data['id'] = new_id
        self.update_user(new_id, **data)
        return new_id
    
# ------
    
        
    def get_task_data(self, task_id: int) -> dict:
        filename = os.path.join(self.task_dir, f"{task_id}.json")
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as f:
            data = json.load(f)
            return data
        
    def find_tasks(self, **kwargs) -> List[dict]:
        result = []
        for filename in os.listdir(self.task_dir):
            task_id = int(filename[:filename.find('.')])
            data = self.get_task_data(task_id)
            if all([data.get(k) == v for k, v in kwargs.items()]):
                result.append(data)
        return result
        
    def update_task(self, task_id: int, **data):
        filename = os.path.join(self.task_dir, f"{task_id}.json")
        if not os.path.exists(filename):
            raise ValueError
        with open(filename, 'w') as f:
            json.dump(data, f, ensure_ascii=True)
            
    def create_task(self, **data):
        new_id = self.get_free_id(self.task_dir)
        data['id'] = new_id
        self.update_task(new_id, **data)
        return new_id
    
    def delete_task(self, task_id: int):
        filename = os.path.join(self.task_dir, f"{task_id}.json")
        if os.path.exists(filename):
            os.remove(filename)


    
