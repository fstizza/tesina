import { AccountFactory } from "./account/factory.js";
import { MovementsAccount } from "./account/movementsAccount.js";
import { ATM } from "./atm.js";
import { ValidatePassword } from "./user/password.js";
import { UserFactory } from "./user/factory.js";
import { ChangePassword } from "./user/changePassword.js";

export class Manager {
  /**
   * @type {Object.<string, ChangePassword>} users
   */
  users;
  /**
   * @type {ATM} atm
   */
  atm;
  /**
   * @type {Object.<string, MovementsAccount>} accounts
   */
  accounts;

  constructor(atm, users, accounts) {
    this.atm = atm;
    this.users = users;
    this.accounts = accounts;
  }

  getUser(uid, password) {
    const user = this.users[uid];
    if (!user) {
      throw Error("Usuario no encontrado");
    }
    if (!user.authenticate(password)) {
      throw Error("Clave incorrecta");
    }
    return user;
  }

  authenticateAdmin(admin, adminpsswd) {
    if (!this.atm.authenticateAdmin(admin, adminpsswd)) {
      throw Error("Credenciales de admin incorrectas");
    }
  }

  withdraw(uid, password, amount) {
    this.getUser(uid, password);

    this.atm.withdraw(amount);
    try {
      const account = this.accounts[uid];
      account.withdraw(amount);
    } catch (error) {
      this.atm.deposit(amount); // Rollback the withdraw of the atm
      throw error;
    }
  }

  deposit(uid, password, amount) {
    this.getUser(uid, password);

    this.atm.deposit(amount);
    const account = this.accounts[uid];
    account.deposit(amount);
  }

  changePassword(uid, password, newPassword) {
    const user = this.getUser(uid, password);
    user.changePassword(newPassword);
  }

  getBalance(uid, password) {
    const _ = this.getUser(uid, password);
    return this.accounts[uid].getBalance();
  }

  newUser(admin, adminpsswd, uid, password, name, salary, balance) {
    this.authenticateAdmin(admin, adminpsswd);

    if (this.users[uid]) {
      throw Error("Ya existe el usuario");
    }

    if (Object.entries(this.users).length === 5) {
      throw Error("Maxima cantidad de usuarios alcanzados");
    }

    if (salary !== balance) {
      throw Error("El saldo inicial debe ser igual al sueldo declarado");
    }

    if (!ValidatePassword(password)) {
      throw Error("El formato de la clave no es valido");
    }

    const user = UserFactory.createNewUser(name, password);
    const account = AccountFactory.createNewAccount(balance, salary);

    this.users[uid] = user;
    this.accounts[uid] = account;
  }

  loadATM(admin, adminpsswd, amount) {
    this.authenticateAdmin(admin, adminpsswd);

    this.atm.deposit(amount);
  }

  getMovements(admin, adminpsswd, uid, from, to) {
    this.authenticateAdmin(admin, adminpsswd);
    const account = this.accounts[uid];
    if (!account) {
      throw Error("El usuario no existe");
    }
    return account.getMovements(from, to);
  }

  static fromObject(json) {
    const atm = json.atm;
    const atmInstance = new ATM(atm.balance, atm.admin, atm.password);
    const users = json.users;
    const usersInstance = Object.entries(users).reduce((acum, current) => {
      const [uid, userLastChange] = current;
      const user = userLastChange.user;
      return {
        [uid]: UserFactory.createNewUser(
          user.name,
          user.password,
          userLastChange.lastPasswordChange
        ),
        ...acum,
      };
    }, {});
    const accounts = json.accounts;
    const accountsInstance = Object.entries(accounts).reduce(
      (acum, current) => {
        const [uid, movAccount] = current;
        const account = movAccount.account.account;
        return {
          [uid]: AccountFactory.createNewAccount(
            account.balance,
            account.salary,
            movAccount.movements,
            movAccount.movementsToday,
            movAccount.lastMovement
          ),
          ...acum,
        };
      },
      {}
    );
    return new Manager(atmInstance, usersInstance, accountsInstance);
  }
}
