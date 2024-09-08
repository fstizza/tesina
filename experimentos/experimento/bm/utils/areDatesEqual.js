const areDatesEqual = (date1, date2) => {
  const formattedDate1 = date1.split('T')[0];
  const formattedDate2 = date2.split('T')[0];

  return formattedDate1 === formattedDate2;
};

export default areDatesEqual;
