const isDatesMonthEqual = (date1, date2) => {
  const formattedDate1 = new Date(date1)
  const formattedDate2 = new Date(date2);

  return formattedDate1.getMonth() === formattedDate2.getMonth() 
    && formattedDate1.getFullYear() === formattedDate2.getFullYear();
};

export default isDatesMonthEqual;
