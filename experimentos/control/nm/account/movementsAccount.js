import dayjs from "dayjs";
import { Account } from "./account.js";
import { LimitedWithdraw } from "./limitedWithdraw.js";

export class MovementsAccount extends Account {
  /**
   * @typedef {{
   *  amount: number,
   *  date: Date,
   *  operation: ("withdraw" | "deposit")
   * }} Movement
   * @type {Movement[]} movements
   */
  movements;

  /**
   * @type {number} movementsToday
   */
  movementsToday;

  /**
   * @type {Date} lastMovement
   */
  lastMovement;

  /**
   * @type {Account} account
   */
  account;

  /**
   * @constructor
   * @param {Account} [account
   * @param {Movement[]} [movements]
   * @param {number} [movementsToday]
   * @param {Date} [lastMovement]
   */
  constructor(account, movements = [], movementsToday = 0, lastMovement) {
    super();
    this.movements = movements;
    this.movementsToday = movementsToday;
    this.lastMovement = lastMovement;
    this.account = account;
  }

  /**
   * @private
   * @param {Date} today
   */
  validateMovement(today) {
    if (this.lastMovement === undefined) {
      this.lastMovement = today;
      this.movementsToday = 0;
    } else {
      const lastM = dayjs(this.lastMovement);
      if (!dayjs(today).isSame(lastM, "day")) {
        this.lastMovement = today;
        this.movementsToday = 0;
      }
    }

    if (this.movementsToday === 3) {
      throw Error("Maxima cantidad de movimientos por dia alcanzado");
    }
  }

  /**
   * @param {number} amount
   */
  withdraw(amount) {
    const today = new Date();

    this.validateMovement(today);

    this.account.withdraw(amount);

    this.movementsToday++;

    this.movements.push({
      amount: amount,
      date: today,
      operation: "withdraw",
    });
  }

  /**
   * @param {number} amount
   */
  deposit(amount) {
    const today = new Date();

    this.validateMovement(today);

    this.account.deposit(amount);

    this.movementsToday++;

    this.movements.push({
      amount: amount,
      date: today,
      operation: "deposit",
    });
  }

  /**
   * @returns {Movement[]} movements
   */
  getMovements(from, to) {
    return this.movements.filter((m) => dayjs(m.date).isAfter(dayjs(from), 'D') && dayjs(m.date).isBefore(dayjs(to), 'D'));
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
   * @returns {MovementsAccount}
   */
  static fromObject(object) {
    const account = LimitedWithdraw.fromObject(object.account);
    return new MovementsAccount(
      account,
      object.movements,
      object.movementsToday,
      object.lastMovement
    );
  }
}
