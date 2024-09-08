/**
 * @param {string} password 
 * @returns {bool} valid
 */
export function ValidatePassword(password) {
    return password.length >= 8 && /^[a-zA-Z0-9]+$/.test(password)
}