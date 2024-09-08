import { Account } from "./account.js";

export class LimitedWithdraw extends Account {
  /**
   * @type {Account} account
   */
  account;

  /**
   * @constructor
   * @param {Account} account
   */
  constructor(account) {
    super();
    this.account = account;
  }

  /**
   * @param {number} amount
   */
  withdraw(amount) {
    if (amount * 2 > this.account.salary) {
      throw Error("Monto excede a la mitad del salario");
    }
    this.account.withdraw(amount);
  }

  /**
   * @param {number} amount
   */
  deposit(amount) {
    this.account.deposit(amount);
  }

  /**
   * @returns {number} balance
   */
  getBalance() {
    return this.account.getBalance();
  }

  /**
   * @returns {number} salary
   */
  getSalary() {
    return this.account.salary;
  }

  /**
   * @param {Object} object
   * @returns {LimitedWithdraw}
   */
  static fromObject(object) {
    const a = Account.fromObject(object.account);
    return new LimitedWithdraw(a);
  }
}
