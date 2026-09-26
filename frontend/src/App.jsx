import { useState } from "react";
import "./App.css";

const API = "http://localhost:8000";

function App() {

  const [files, setFiles] = useState([]);

  const [data, setData] = useState([]);

  const [columns, setColumns] = useState([]);

  const [stats, setStats] = useState({
    extracted: 0,
    transformed: 0,
    loaded: 0
  });

  const [status, setStatus] = useState(
    "Ready"
  );

  const [loading, setLoading] = useState(false);


  // ------------------------------------------
  // UPLOAD + EXTRACT
  // ------------------------------------------

  const uploadFiles = async () => {

    if (!files.length) {

      alert(
        "Please select CSV files"
      );

      return;
    }

    const formData = new FormData();

    files.forEach((file) => {

      formData.append(
        "files",
        file
      );

    });

    try {

      setLoading(true);

      setStatus(
        "Extracting data..."
      );

      const response = await fetch(
        `${API}/upload`,
        {
          method: "POST",
          body: formData
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        throw new Error(
          result.detail ||
          "Upload failed"
        );

      }

      setData(
        result.preview
      );

      setColumns(
        result.columns
      );

      setStats({
        extracted: result.rows,
        transformed: 0,
        loaded: 0
      });

      setStatus(
        "Extraction completed"
      );

    } catch (error) {

      alert(error.message);

      setStatus("Error");

    } finally {

      setLoading(false);

    }
  };


  // ------------------------------------------
  // TRANSFORM
  // ------------------------------------------

  const transformData = async () => {

    try {

      setLoading(true);

      setStatus(
        "Transforming data..."
      );

      const response = await fetch(
        `${API}/transform`,
        {
          method: "POST"
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        throw new Error(
          result.detail ||
          "Transformation failed"
        );

      }

      setData(
        result.preview
      );

      setColumns(
        result.columns
      );

      setStats((previous) => ({

        ...previous,

        transformed:
          result.after_rows

      }));

      setStatus(
        "Transformation completed"
      );

    } catch (error) {

      alert(error.message);

      setStatus("Error");

    } finally {

      setLoading(false);

    }
  };


  // ------------------------------------------
  // LOAD
  // ------------------------------------------

  const loadData = async () => {

    try {

      setLoading(true);

      setStatus(
        "Loading data into MySQL..."
      );

      const response = await fetch(
        `${API}/load`,
        {
          method: "POST"
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        throw new Error(
          result.detail ||
          "Database loading failed"
        );

      }

      setStats((previous) => ({

        ...previous,

        loaded:
          result.rows_loaded

      }));

      setStatus(
        "Data loaded successfully"
      );

    } catch (error) {

      alert(error.message);

      setStatus("Error");

    } finally {

      setLoading(false);

    }
  };


  // ------------------------------------------
  // COMPLETE PIPELINE
  // ------------------------------------------

  const runPipeline = async () => {

    try {

      setLoading(true);

      setStatus(
        "Running complete ETL pipeline..."
      );

      const response = await fetch(
        `${API}/run`,
        {
          method: "POST"
        }
      );

      const result =
        await response.json();

      if (!response.ok) {

        throw new Error(
          result.detail ||
          "Pipeline failed"
        );

      }

      setData(
        result.preview
      );

      setColumns(
        result.columns
      );

      setStats({

        extracted:
          result.extracted_rows,

        transformed:
          result.transformed_rows,

        loaded:
          result.loaded_rows

      });

      setStatus(
        "ETL pipeline completed successfully"
      );

    } catch (error) {

      alert(error.message);

      setStatus("Error");

    } finally {

      setLoading(false);

    }
  };


  return (

    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="logo">

          <div className="logo-icon">
            ETL
          </div>

          <div>

            <h2>
              DataFlow
            </h2>

            <span>
              ETL Pipeline
            </span>

          </div>

        </div>


        <nav>

          <div className="nav-item active">
            <span>▣</span>
            Pipeline
          </div>

          <div className="nav-item">
            <span>◉</span>
            Data Preview
          </div>

          <div className="nav-item">
            <span>▤</span>
            Database
          </div>

        </nav>


        <div className="sidebar-bottom">

          <span className="status-dot"></span>

          API Connected

        </div>

      </aside>


      {/* MAIN */}

      <main className="main">

        <header>

          <div>

            <h1>
              ETL Pipeline
            </h1>

            <p>
              Extract, transform and load
              your customer data
            </p>

          </div>


          <div className="api-status">

            <span></span>

            FastAPI Connected

          </div>

        </header>


        {/* STATISTICS */}

        <section className="stats">

          <div className="stat-card">

            <div className="stat-icon">
              ↓
            </div>

            <div>

              <span>
                Extracted
              </span>

              <strong>
                {stats.extracted}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              ⚙
            </div>

            <div>

              <span>
                Transformed
              </span>

              <strong>
                {stats.transformed}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              ↑
            </div>

            <div>

              <span>
                Loaded
              </span>

              <strong>
                {stats.loaded}
              </strong>

            </div>

          </div>


          <div className="stat-card">

            <div className="stat-icon">
              ✓
            </div>

            <div>

              <span>
                Status
              </span>

              <strong className="success">
                {status}
              </strong>

            </div>

          </div>

        </section>


        {/* PIPELINE */}

        <section className="pipeline-card">

          <div className="section-title">

            <div>

              <h2>
                Pipeline
              </h2>

              <p>
                Process your CSV data
              </p>

            </div>

          </div>


          <div className="steps">

            {/* EXTRACT */}

            <div className="step">

              <div className="step-number">
                01
              </div>

              <h3>
                Extract
              </h3>

              <p>
                Upload CSV files
              </p>

              <input
                type="file"
                accept=".csv"
                multiple
                onChange={(event) =>
                  setFiles(
                    Array.from(
                      event.target.files
                    )
                  )
                }
              />

              <button
                onClick={uploadFiles}
                disabled={loading}
              >
                Upload & Extract
              </button>

            </div>


            <div className="connector">
              →
            </div>


            {/* TRANSFORM */}

            <div className="step">

              <div className="step-number">
                02
              </div>

              <h3>
                Transform
              </h3>

              <p>
                Clean and normalize data
              </p>

              <div className="transform-list">

                <span>
                  ✓ Remove duplicates
                </span>

                <span>
                  ✓ Remove empty rows
                </span>

                <span>
                  ✓ Clean columns
                </span>

                <span>
                  ✓ Normalize names
                </span>

                <span>
                  ✓ Normalize emails
                </span>

                <span>
                  ✓ Validate age
                </span>

              </div>

              <button
                onClick={transformData}
                disabled={loading}
              >
                Transform Data
              </button>

            </div>


            <div className="connector">
              →
            </div>


            {/* LOAD */}

            <div className="step">

              <div className="step-number">
                03
              </div>

              <h3>
                Load
              </h3>

              <p>
                Store data in MySQL
              </p>

              <div className="database-box">

                <strong>
                  MySQL
                </strong>

                <span>
                  etlpipeline.customers
                </span>

              </div>

              <button
                onClick={loadData}
                disabled={loading}
              >
                Load to Database
              </button>

            </div>

          </div>


          <div className="run-container">

            <button
              className="run-button"
              onClick={runPipeline}
              disabled={loading}
            >

              {loading
                ? "Processing..."
                : "▶ Run Complete Pipeline"}

            </button>

          </div>

        </section>


        {/* DATA PREVIEW */}

        <section className="data-card">

          <div className="data-header">

            <div>

              <h2>
                Data Preview
              </h2>

              <p>
                Showing current dataset
              </p>

            </div>


            <span className="record-count">

              {data.length}
              {" "}
              records

            </span>

          </div>


          <div className="table-wrapper">

            {data.length === 0 ? (

              <div className="empty">

                <div>
                  📂
                </div>

                <h3>
                  No data yet
                </h3>

                <p>
                  Upload a CSV file
                  to begin
                </p>

              </div>

            ) : (

              <table>

                <thead>

                  <tr>

                    {columns.map(
                      (column) => (

                        <th
                          key={column}
                        >
                          {column}
                        </th>

                      )
                    )}

                  </tr>

                </thead>


                <tbody>

                  {data.map(
                    (row, index) => (

                      <tr key={index}>

                        {columns.map(
                          (column) => (

                            <td
                              key={column}
                            >

                              {String(
                                row[column] ??
                                ""
                              )}

                            </td>

                          )
                        )}

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            )}

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;