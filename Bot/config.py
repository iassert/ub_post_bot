
class Config:
    token: str 
    creator_id: int

    post_update_time: str

    post_times: list[str]

    limit: str = len(post_times)

    reset_time_1: str
    reset_time_2: str
