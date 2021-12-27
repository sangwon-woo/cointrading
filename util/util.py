def time_print(start_time, end_time):
    delta = end_time - start_time
    hours = delta // 3600
    minutes = (delta - (hours * 3600)) // 60
    seconds = (delta - (hours * 3600) - (minutes * 60)) % 60
    if hours:
        if minutes:
            print(f'{hours}시간 {minutes}분 {seconds}초')
        else:
            print(f'{hours}시간 {seconds}초')
    else:
        if minutes:
            print(f'{minutes}분 {seconds}초')
        else:
            print(f'{seconds}초')


