import dayjs from "dayjs";
import {User} from "./user.js"

export class ChangePassword extends User {
  user;

  lastPasswordChange;

  constructor(user, lastChange) {
    super()
    this.user = user;
    this.lastPasswordChange = lastChange;
  }

  authenticate(password) {
    return this.user.authenticate(password);
  }

  changePassword(password) {
    const today = new Date();
    const previous = this.lastPasswordChange
    if (previous === undefined) {
        this.lastPasswordChange = today;
    } else {
      const lastC = dayjs(previous);
      if (dayjs(today).isSame(lastC, "M")) {
        throw Error("Solo un cambio de clave por mes esta permitido");
      }
      this.lastPasswordChange = today;
    }
    try {
        this.user.changePassword(password)
    } catch (error) {
        this.lastPasswordChange = previous
        throw error
    }
  }
}
