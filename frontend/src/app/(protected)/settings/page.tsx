'use client'

import { useState, useEffect } from 'react'
import { fetchCompetitors, fetchProducts } from '@/lib/api'

export default function SettingsPage() {
    const [competitors, setCompetitors] = useState<any[]>([])
    const [products, setProducts] = useState<any[]>([])
    const [loading, setLoading] = useState(true)

    // Form states
    const [newCompName, setNewCompName] = useState('')
    const [newProdName, setNewProdName] = useState('')
    const [newProdTA, setNewProdTA] = useState('')

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        setLoading(true)
        try {
            const [c, p] = await Promise.all([fetchCompetitors(), fetchProducts()])
            setCompetitors(c)
            setProducts(p)
        } finally {
            setLoading(false)
        }
    }

    const handleAddCompetitor = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!newCompName) return

        await fetch('http://127.0.0.1:8000/api/competitors', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newCompName, tier: 'Tier 1' })
        })
        setNewCompName('')
        loadData()
    }

    const handleAddProduct = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!newProdName) return

        await fetch('http://127.0.0.1:8000/api/products', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: newProdName,
                therapeutic_area: newProdTA,
                indication: 'New Indication',
                phase: 'Marketed'
            })
        })
        setNewProdName('')
        setNewProdTA('')
        loadData()
    }

    const handleDeleteCompetitor = async (id: number) => {
        await fetch(`http://127.0.0.1:8000/api/competitors/${id}`, { method: 'DELETE' })
        loadData()
    }

    const handleDeleteProduct = async (id: number) => {
        await fetch(`http://127.0.0.1:8000/api/products/${id}`, { method: 'DELETE' })
        loadData()
    }

    return (
        <div className="main-content">
            <div className="top-bar">
                <h1>Settings & Portfolio</h1>
                <p className="subtitle">Manage Eli Lilly's focus assets and competitive watchlist.</p>
            </div>

            <div className="content-grid">
                {/* Competitors Section */}
                <section className="dashboard-section">
                    <h2>Tracked Competitors</h2>
                    <div className="card">
                        <form onSubmit={handleAddCompetitor} className="flex gap-4 mb-6">
                            <input
                                type="text"
                                placeholder="Competitor Name (e.g. Novo Nordisk)"
                                className="flex-1 p-2 border rounded"
                                value={newCompName}
                                onChange={(e) => setNewCompName(e.target.value)}
                            />
                            <button type="submit" className="btn-primary" style={{ width: 'auto', padding: '0.5rem 1.5rem' }}>
                                Add Competitor
                            </button>
                        </form>

                        <div className="space-y-2">
                            {competitors.map(c => (
                                <div key={c.id} className="flex justify-between items-center p-3 bg-gray-50 rounded border border-gray-100">
                                    <span className="font-semibold text-gray-800">{c.name}</span>
                                    <button
                                        onClick={() => handleDeleteCompetitor(c.id)}
                                        className="text-red-600 text-sm hover:underline"
                                    >
                                        Delete
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Products Section */}
                <section className="dashboard-section">
                    <h2>Tracked Products</h2>
                    <div className="card">
                        <form onSubmit={handleAddProduct} className="flex flex-col gap-4 mb-6">
                            <div className="flex gap-4">
                                <input
                                    type="text"
                                    placeholder="Product Name (e.g. Mounjaro)"
                                    className="flex-1 p-2 border rounded"
                                    value={newProdName}
                                    onChange={(e) => setNewProdName(e.target.value)}
                                />
                                <input
                                    type="text"
                                    placeholder="Therapeutic Area"
                                    className="flex-1 p-2 border rounded"
                                    value={newProdTA}
                                    onChange={(e) => setNewProdTA(e.target.value)}
                                />
                            </div>
                            <button type="submit" className="btn-primary" style={{ width: 'auto', alignSelf: 'flex-start', padding: '0.5rem 1.5rem' }}>
                                Add Product
                            </button>
                        </form>

                        <div className="space-y-2">
                            {products.map(p => (
                                <div key={p.id} className="flex justify-between items-center p-3 bg-gray-50 rounded border border-gray-100">
                                    <div>
                                        <span className="font-semibold text-gray-800">{p.name}</span>
                                        <span className="ml-3 text-xs text-gray-500">{p.therapeutic_area}</span>
                                    </div>
                                    <button
                                        onClick={() => handleDeleteProduct(p.id)}
                                        className="text-red-600 text-sm hover:underline"
                                    >
                                        Delete
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                </section>
            </div>
        </div>
    )
}
