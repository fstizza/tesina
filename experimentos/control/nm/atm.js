/** Modelo que representa un usuario.
 * @class
 */
 export class ATM {
    /** 
     * @type {string} admin
    */
    admin

    /** 
     * @type {string} password
    */
    password

    /** 
     * @type {number} balance
    */
    balance

    /**
     * @constructor
     * @param {number} [balance] 
     * @param {string} [admin] 
     * @param {string} [password] 
     */
    constructor(balance=0, admin="00000000", password="changeme") {
        this.admin = admin
        this.password = password
        this.balance = balance
    }

    withdraw(amount) {
        if(amount > this.balance) {
            throw Error("No hay suficiente dinero en el cajero.")
        }
        this.balance -= amount
    }

    deposit(amount) {
        this.balance += amount
    }

    authenticateAdmin(user, password) {
        return user === this.admin && password === this.password
    }
}