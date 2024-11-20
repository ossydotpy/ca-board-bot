def is_valid_contract_address(address):
    """Basic validation for Solana address"""
    return (
        32<=len(address) <= 44 and 
        all(char in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' for char in address)
    ) or len(address) == 56
