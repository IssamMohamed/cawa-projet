import { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [students, setStudents] = useState(null);
  const [render, setReander] = useState(false)
  const [student, setStudent] = useState({
    full_name: '',
    birth_date: '',
    faculty: '',
    specialty: '',
    matricule_id: '',
    year_of_study: '',
    college: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setStudent((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const createStudent = async () => {
    try {
      const payload = {
        ...student,
        year_of_study: Number(student.year_of_study)
      };
  
      console.log(payload);
  
      const response = await fetch('http://127.0.0.1:5000/students/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        throw new Error(`Failed to create student. Status: ${response.status}`);
      }
  
      const newStudent = await response.json();
      setReander(!render);
      if (!newStudent) {
        throw new Error(`Failed to create student. Status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error creating student:', error);
    }
  };
  


 
  
  

  
  useEffect(() => {
    const getStudents = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/students/");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setStudents(data);
      } catch (err) {
        console.error('Fetch error:', err);
      }
    };

    getStudents();
  }, [render]);  

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/students/${id}`, {
        method: 'DELETE',
      });
  
      if (!response.ok) {
        throw new Error(`Failed to delete student with ID ${id}. Status: ${response.status}`);
      }
  
      // Optionally update the UI
      setStudents((prevStudents) => prevStudents.filter(student => student.id !== id));
      console.log(`Student with ID ${id} deleted successfully.`);
      setReander(!render);
    } catch (error) {
      console.error('Error deleting student:', error);
    }
  };

  return (
    <div className='w-full h-full  flex flex-col justify-center items-center pt-40'>
      <h1 className="text-3xl font-bold text-red-400 pb-20">Students Labiry</h1>

       
      <div className="w-4/5 mx-auto my-4 p-4 border rounded-lg bg-gray-100 space-y-3">
      <input name="full_name"  value={student.full_name} onChange={handleChange} placeholder="Full Name" className="w-full p-2 border rounded" />
      <input name="birth_date"  value={student.birth_date} onChange={handleChange} placeholder="Birth Date (YYYY-MM-DD)" className="w-full p-2 border rounded" />
      <input name="college" value={student.college} onChange={handleChange} placeholder="College" className="w-full p-2 border rounded" />
      <input name="faculty" value={student.faculty} onChange={handleChange} placeholder="Faculty" className="w-full p-2 border rounded" />
      <input name="matricule_id" value={student.matricule_id} onChange={handleChange} placeholder="Matricule ID" className="w-full p-2 border rounded" />
      <input name="specialty" value={student.specialty} onChange={handleChange} placeholder="Specialty" className="w-full p-2 border rounded" />
      <input name="year_of_study" type='number' value={student.year_of_study} onChange={handleChange} placeholder="Year of Study" className="w-full p-2 border rounded" />
      <button onClick={createStudent} className="bg-blue-500 text-white px-4 py-2 rounded">
        Create Student
      </button>
    </div>
       

      <div className="space-y-4 w-full py-30">
      {students ? (
  students.map((student) => (
    <div
      key={student.id}
      className="w-4/5 mx-auto border border-gray-300 rounded-xl p-4 bg-white shadow-sm flex justify-between items-center hover:scale-105 hover:bg-gray-600 hover:text-white transition-all duration-300"
    >
      <div className='flex justify-around items-center w-4/5'>
        <div>
          <p className="text-md font-medium mt-2">Full name: {student.full_name}</p>
          <p className="text-sm">Matricule: {student.matricule_id}</p>
        </div>
        <div>
        <p className="text-md font-medium mt-2">Faculty: {student.faculty}</p>
        <p className="text-sm ">Specialty: {student.specialty}</p>
        </div>
        <div>
          <p className="text-md font-medium mt-2">College: {student.college}</p>
          <p className="text-sm ">Years of study: {student.year_of_study}</p>
        </div>
      </div>
      <button
        className="bg-red-500  text-white px-4 py-2 rounded-lg hover:scale-105 hover:bg-violet-500 transition-all duration-300"
        onClick={() => handleDelete(student.id)}
      >
        Delete
      </button>
    </div>
  ))
) : (
  <p className="text-gray-500 text-lg mt-4">Loading students...</p>
)}

</div>
    </div>
  );
}

export default App;
