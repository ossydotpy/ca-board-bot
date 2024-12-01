from datetime import datetime


def is_valid_contract_address(address):
    """Basic validation for Solana address"""
    return (
        32<=len(address) <= 44 and 
        all(char in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' for char in address)
    )


def time_ago(timestamp_str):

    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    
    difference = datetime.now() - timestamp
    
    if difference.days > 0:
        return f"{difference.days} days ago"
    elif difference.seconds > 3600:
        hours = difference.seconds // 3600
        return f"{hours} hours ago"
    elif difference.seconds > 60:
        minutes = difference.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return f"{difference.seconds} seconds ago"
    

if __name__=='__main__':

    print(time_ago('2024-12-01 09:19:08'))