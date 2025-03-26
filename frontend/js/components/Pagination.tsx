interface PaginationProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
    if (totalPages <= 1) return null;   // Oculta paginação se houver apenas uma página

    const handlePageChange = (page: number) => {
        if (page >= 1 && page <= totalPages) {
            onPageChange(page);
        }
    };

    return (
        <div className="pagination-container d-flex justify-content-center space-x-2 mt-4">
            {/* Botão Anterior */}
            <button 
                onClick={() => handlePageChange(currentPage -1)}
                disabled={currentPage === 1}
                className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
            >
            {"⤺"}
            </button>

            {/* Números das Páginas */}
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                    key={page}
                    onClick={() => handlePageChange(page)}
                    className={`px-3 py-1 rounded ${
                        currentPage === page ? "bg-success text-white" : "bg-gray-200"
                    }`}
                >
                    {page}
                </button>
            ))}

            {/* Botão Próximo */}
            <button
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
            >
                {"⤻"}
            </button>
        </div>
    );
};

export default Pagination;
