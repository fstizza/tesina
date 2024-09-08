/** Modelo que representa un usuario.
 * @class
 */
export class Account {
  /**
   * @type {number} balance
   */
  balance;

  /**
   * @type {number} salary
   */
  salary;

  /**
   * @constructor
   * @param {number} [balance]
   * @param {number} [salary]
   */
  constructor(balance = 0, salary = 0) {
    this.balance = balance;
    this.salary = salary;
  }

  /**
   * @param {number} amount
   */
  withdraw(amount) {
    if (amount > this.balance) {
      throw Error("Monto insuficiente");
    }
    this.balance -= amount;
  }

  /**
   * @param {number} amount
   */
  deposit(amount) {
    this.balance += amount;
  }

  /**
   * @returns {number} balance
   */
  getBalance() {
    return this.balance;
  }
  /**
   * @returns {number} salary
   */
  getSalary() {
    return this.salary;
  }

  /**
   * @param {Object} object
   * @returns {Account}
   */
  static fromObject(object) {
    return new Account(object.balance, object.salary);
  }
}
